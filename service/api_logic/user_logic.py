from flask import current_app, url_for, jsonify, make_response
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from dto.api_input import UpdateUserPreferencesDTO
from dto.api_output import OutputSportPreferences, OutputTeamPreferences
from exept.exeptions import IncorrectPreferencesError, IncorrectTypeOfPreferencesError, SignatureExpiredError, \
    IncorrectSignatureError
from dto.api_input import InputUserLogInDTO
from dto.api_output import OutputUser, OutputLogin
from database.models import User
from dto.common_response import CommonResponse, CommonResponseWithUser
from exept.exeptions import UserDoesNotExistError, UserAlreadyExistError
import bcrypt
from logger.logger import Logger
from jinja2 import Environment, FileSystemLoader
import os
from flask_jwt_extended import create_access_token,create_refresh_token, set_access_cookies, set_refresh_cookies, decode_token
from service.api_logic.auth_strategy import AuthManager
from database.postgres.dto.jwt import jwtDTO
from database.postgres.dto.refresh import refreshDTO
from datetime import datetime
from api.refresh_token_logic import get_client_ip, get_country_from_ip, get_user_device, generate_nonce
from flask_jwt_extended import get_jwt_identity, get_jwt
from service.api_logic.models.api_models import SportPreferenceFields, TeamPreferenceFields
from api.refresh_token_logic import UserInfo


SPORT_TYPE = "sport"
TEAM_TYPE = "team"

class UserService:

    def __init__(self, user_dal, preferences_dal, sport_dal, jwt_dal, refresh_dal):
        self._user_dal = user_dal
        self._jwt_dal = jwt_dal
        self._refresh_dal = refresh_dal
        self._preferences_dal = preferences_dal
        self._sport_dal = sport_dal
        self._serializer = URLSafeTimedSerializer(current_app.secret_key)
        self._logger = Logger("logger", "all.log").logger


    def get_user_by_email_or_username(self, email=None, username=None):
        return self._user_dal.get_user_by_email_or_username(email, username)


    def get_existing_user(self, email=None, username=None):
        return self._user_dal.get_existing_user(email, username)


    async def sign_up_user(self, email, username, password):
        existing_user = self.get_existing_user(email = email, username = username)
        if existing_user:
            self._logger.debug("User already exist")
            raise UserAlreadyExistError()

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        new_user = User(email = email, username = username, password_hash = hashed_password.decode('utf-8'))
        self.create_user(new_user)
        token = await self.get_generate_auth_token(new_user)

        return OutputLogin(email = new_user.email, token = token, id = new_user.user_id)


    def create_user(self, new_user):
        return self._user_dal.create_user(new_user)


    def request_password_reset(self, email: str):
        existing_user = self.get_user_by_email_or_username(email = email)
        if not existing_user:
            raise UserDoesNotExistError(email)

        token = self.__get_reset_token(existing_user.email)

        return self.__send_reset_email(existing_user, token)


    def __message_to_user_gmail(self, user: User, reset_url):
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        env = Environment(loader = FileSystemLoader(template_dir))
        template = env.get_template("reset_password_email.html")

        return template.render(username = user.username, reset_url = reset_url)


    def __send_reset_email(self, user: User, token: str):
        reset_url = url_for('login_app.reset_password', token = token, _external = True)
        msg = Message(
            'Password Reset Request',
            sender = current_app.config['MAIL_USERNAME'],
            recipients = [user.email],
            html = self.__message_to_user_gmail(user, reset_url)
        )
        current_app.extensions['mail'].send(msg)

        return CommonResponse().to_dict()


    def __get_reset_token(self, email) -> str:
        user = self.get_user_by_email_or_username(email = email)
        if not user:
            raise UserDoesNotExistError(email)

        return self._serializer.dumps(user.username, salt = "email-confirm")


    def reset_user_password(self, token, new_password: str):
        username = self.confirm_token(token)
        user = self.get_user_by_email_or_username(username = username)
        if not user:
            raise UserDoesNotExistError(username)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)

        self._user_dal.update_user_password(user, hashed_password.decode('utf-8'))
        new_jwt = create_access_token(identity=user.email)
        new_refresh = create_refresh_token(identity=user.email)

        response = jsonify({"message": "Password reset successful"})
        set_access_cookies(response, new_jwt)
        set_refresh_cookies(response, new_refresh)

        return response


    def confirm_token(self, token: str, expiration=3600):
        try:
            user = self._serializer.loads(token, salt = "email-confirm", max_age = expiration)
            return user

        except SignatureExpired:
            raise SignatureExpiredError()
        except BadSignature:
            raise IncorrectSignatureError()


    async def log_in(self, credentials: InputUserLogInDTO):
        login_context = AuthManager(self)
        user = await login_context.execute_log_in(credentials)
        response = await self.create_access_token_response(user)
        return response

    async def __generate_auth_token(self, user, salt):
        return self._serializer.dumps(user.email, salt = salt)


    async def get_generate_auth_token(self, user):
        return await self.__generate_auth_token(user, salt = "user-auth-token")


    async def save_tokens_to_db(self, user, access_token: str, refresh_token: str):
        user_info = UserInfo()
        
        decode_access_token = decode_token(access_token)
        decode_refresh_token = decode_token(refresh_token)
        
        access_expires_at = datetime.utcfromtimestamp(decode_access_token['exp'])
        refresh_expires_at = datetime.utcfromtimestamp(decode_refresh_token['exp'])


        access_jwt_dto = jwtDTO(
            user_id=user.id,
            jti=decode_access_token['jti'],   
            token_type="access",
            revoked=False,
            expires_at=access_expires_at
        )
        self._jwt_dal.save_jwt(access_jwt_dto)


        refresh_jwt_dto = jwtDTO(
            user_id=user.id,
            jti=decode_refresh_token['jti'],
            token_type="refresh",
            revoked=False,
            expires_at=refresh_expires_at  
        )
        self._jwt_dal.save_jwt(refresh_jwt_dto)


        refresh_dto = refreshDTO(
            user_id=user.id,
            last_ip=user_info.get_country_from_ip(),
            last_device= user_info.get_user_device(),
            nonce=user_info.generate_nonce()
        )
        self._refresh_dal.save_refresh_token(refresh_dto)


    async def create_access_token_response(self, user, return_tokens: bool = False):


        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)

        await self.save_tokens_to_db(user, access_token, refresh_token)

    
        response_data = {
            "user_id": user.id,
            "user_email": user.email
        }
        if return_tokens:
            response_data["access_token"] = access_token
            response_data["refresh_token"] = refresh_token

        response = make_response(jsonify(response_data))
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response
    
    async def verify_nonce(self, user_email: str, token_nonce: str) -> bool:
        user = await self._user_dal.get_user_by_email(user_email)
        saved_nonce = self._refresh_dal.get_nonce_by_user_id(user.id)

        return saved_nonce == token_nonce
    
    async def create_new_access_token(self, user_email: str, username: str, refresh: bool = False):
        user_email = await self._user_dal.get_user_by_email(user_email)
        username = await self._user_dal.get_user_by_name(username)
        additional_claims = {
            "email":user_email,
            "username":username
        }
        new_access_token = create_access_token(identity=user_email.email, additional_claims=additional_claims)
        new_refresh_token = create_refresh_token(identity=user_email.email, additional_claims={"nonce": generate_nonce()})
        
        return new_access_token, new_refresh_token

    async def update_refresh_token(self, user_email: str, new_refresh_token: str):
        user = await self._user_dal.get_user_by_email(user_email)
        
        refresh_dto = refreshDTO(
            user_id=user.id,
            last_ip=get_country_from_ip(get_client_ip()),
            last_device=get_user_device(),
            refresh_token=new_refresh_token,
            nonce=generate_nonce()
        )

        self._refresh_dal.update_refresh_token(user.id, refresh_dto)

    async def refresh_tokens(self):
        identity = get_jwt_identity()   
        current_refresh_token = get_jwt()

        token_nonce = current_refresh_token.get("nonce")

        if not self._refresh_dal.verify_nonce(identity, token_nonce):
            return jsonify({"msg": "Invalid refresh token"}), 401

        new_access_token, new_refresh_token = await self.create_new_access_token(identity, refresh=True)

        new_nonce = generate_nonce()
        self._refresh_dal.update_refresh_token(identity, new_refresh_token, new_nonce)

        response = make_response(jsonify({
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }))
    
        set_access_cookies(response, new_access_token)
        set_refresh_cookies(response, new_refresh_token)
 
        return response
    
    def add_preferences(self, dto: UpdateUserPreferencesDTO):
        new_dto_by_type_of_preference = self.dto_for_type_of_preference(dto)

        existing_sports = self._preferences_dal.get_all_sport_preference_indexes()
        if dto.type == SPORT_TYPE:
            valid_preferences = set([sport_id for sport_id in dto.preferences if sport_id in existing_sports])

        if dto.type == TEAM_TYPE:
            valid_preferences = set([team_id for team_id in dto.preferences])

        if not valid_preferences:
            raise IncorrectPreferencesError()

        self.add_valid_user_preferences(new_dto_by_type_of_preference, dto, valid_preferences)

        return CommonResponse().to_dict()


    def get_user_preferences(self, dto: UpdateUserPreferencesDTO):
        new_dto_by_type_of_preference = self.dto_for_type_of_preference(dto)

        prefs = self._preferences_dal.get_user_preferences(new_dto_by_type_of_preference, dto)
        if dto.type == SPORT_TYPE:
            return OutputSportPreferences(many=True).dump(prefs)

        if dto.type == TEAM_TYPE:
            return  OutputTeamPreferences(many=True).dump(prefs)


    def delete_preferences(self, dto: UpdateUserPreferencesDTO):
        new_dto_by_type_of_preference = self.dto_for_type_of_preference(dto)

        self._preferences_dal.delete_user_preferences(new_dto_by_type_of_preference, dto)


    @staticmethod
    def dto_for_type_of_preference(dto):
        if dto.type == SPORT_TYPE:
            return SportPreferenceFields()
        elif dto.type == TEAM_TYPE:
            return TeamPreferenceFields()
        else:
            raise IncorrectTypeOfPreferencesError()


    def get_user_sport_and_club_preferences(self, user_id: int) -> list[int] and list[int] | list[None] and list[None]:
        user_preferences = self._user_dal.get_user_sport_and_club_preferences_by_id(user_id)

        if not user_preferences:
            return [], []

        user_preferred_teams = list({row.preferences for row in user_preferences if row.preferences is not None})
        user_preferred_sports = list({row.sports_id for row in user_preferences if row.sports_id is not None})

        return user_preferred_teams, user_preferred_sports

    def add_valid_user_preferences(self, type_dto, dto, valid_preferences):
        tables_and_cols_dto = self._preferences_dal.getattr_tables_and_columns_by_type(type_dto)

        existing_prefs = [
            pref[0] for pref in self._preferences_dal.get_existing_preferences(dto.user_id, tables_and_cols_dto)
        ]

        new_prefs = [
            tables_and_cols_dto.main_table(**{
                type_dto.user_id_field: dto.user_id,
                type_dto.type_id_field: pref
            })
            for pref in valid_preferences if pref not in existing_prefs
        ]

        if new_prefs:
            self._preferences_dal.insert_new_preferences(new_prefs)

        self.__delete_old_user_preferences(dto, existing_prefs, valid_preferences, tables_and_cols_dto)


    def __delete_old_user_preferences(self, dto, existing_prefs, valid_preferences, tables_and_cols_dto):
        to_delete = [
            pref for pref in existing_prefs if pref not in valid_preferences
        ]

        if to_delete:
            self._preferences_dal.delete_redundant_user_preferences(dto.user_id, to_delete, tables_and_cols_dto)
