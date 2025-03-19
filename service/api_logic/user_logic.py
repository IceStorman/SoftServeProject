from flask import current_app, url_for, jsonify, make_response, request
from user_agents import parse
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from dto.api_input import UpdateUserPreferencesDTO
from dto.api_output import OutputSportPreferences, OutputTeamPreferences
from exept.exeptions import IncorrectPreferencesError, IncorrectTypeOfPreferencesError, SignatureExpiredError, \
    IncorrectSignatureError, InvalidRefreshTokenError
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
from database.postgres.dto.jwt import JwtDTO
from database.postgres.dto.refresh import RefreshTokenDTO
from database.postgres.dto.extended_credentials import ExtendedCredantialsDTO
from database.postgres.dto.additional_claims import AdditionalClaimsDTO
from database.postgres.dto.response_data import ResponseDataDTO
from datetime import datetime
import time
import requests
import hashlib
from  service.api_logic.models.api_models import JTI
from flask_jwt_extended import get_jwt_identity, get_jwt
from service.api_logic.models.api_models import SportPreferenceFields, TeamPreferenceFields




SPORT_TYPE = "sport"
TEAM_TYPE = "team"

class UserService:

    def __init__(self, user_dal, preferences_dal, sport_dal, access_tokens_dal, refresh_dal):
        self._user_dal = user_dal
        self._access_tokens_dal = access_tokens_dal
        self._refresh_dal = refresh_dal
        self._preferences_dal = preferences_dal
        self._sport_dal = sport_dal
        self._serializer = URLSafeTimedSerializer(current_app.secret_key)
        self._logger = Logger("logger", "all.log").logger
        
    @staticmethod    
    def get_user_device() -> str:
        user_agent = request.headers.get("User-Agent", "")
        parsed_agent = parse(user_agent)
        device_info_str = f"Browser: {parsed_agent.browser.family} {parsed_agent.browser.version_string}, " \
                        f"OS: {parsed_agent.os.family} {parsed_agent.os.version_string}, " \
                        f"Device: {parsed_agent.device.family}"
        
        return device_info_str

    def __get_client_ip(self) -> str:
        return request.headers.get("X-Forwarded-For", request.remote_addr)

    def __get_country_from_ip(self) -> str:
        ip = self.__get_client_ip()

        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
            response.raise_for_status()
            unknown = "Unknown"
            return response.json().get("country", unknown)
        except (requests.RequestException, ValueError):
            return unknown

    def has_ip_country_changed(self, stored_country: str) -> bool:
        current_country = self.get_country_from_ip()
        return stored_country != current_country

    def has_device_changed(self, stored_device: str) -> bool:
        current_device = self.get_user_device()
        return stored_device != current_device

    def generate_nonce(self):
        nonce = hashlib.sha256(f"{time.time()}{os.urandom(16)}".encode()).hexdigest()
        return nonce
    
    def is_suspicious_login(self, user_id: int) -> bool:
        refresh_entry = self._refresh_dal.get_valid_refresh_token_by_user(user_id)
        if not refresh_entry:
            return False  

        current_country = self.__get_country_from_ip()
        current_device = self.get_user_device()

        suspicious_conditions = [
            refresh_entry.last_device and refresh_entry.last_device != current_device,
            self._refresh_dal.is_nonce_used(user_id, refresh_entry.nonce)
        ]

        return any(suspicious_conditions)


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
        user = OutputLogin(email = new_user.email, token = new_user, user_id= new_user.user_id, username = new_user.username, new_user = True)
        await self.create_access_token_response(user)


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
        
    async def create_new_access_and_refresh_tokens(self, email: str, username: str,user_id: int,new_user:bool):
        additional_claims = AdditionalClaimsDTO(
            user_id=user_id,
            email=email,
            username=username,
            new_user=new_user
        )
        new_access_token = create_access_token(identity=email.email, additional_claims=additional_claims)
        new_refresh_token = create_refresh_token(identity=email.email, 
                                                 additional_claims=additional_claims.update({"nonce": self.generate_nonce()}))
        
        return new_access_token, new_refresh_token    

    

    async def reset_user_password(self, token, new_password: str):
        username = self.confirm_token(token)
        user = self.get_user_by_email_or_username(username = username)
        if not user:
            raise UserDoesNotExistError(username)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)

        self._user_dal.update_user_password(user, hashed_password.decode('utf-8')) 
        await self.create_access_token_response(user) 
        


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
        user = self._user_dal.get_user_by_email_or_username(email=credentials.email_or_username, username=credentials.email_or_username)
        sus_login = self.is_suspicious_login(user_id=user.user_id)
        if sus_login is True:
            
            ex_access_token, ex_refesh_token = self._refresh_dal.get_valid_tokens_by_user(user_id=user.user_id)
            
            if ex_refesh_token and ex_access_token:
                await login_context.execute_log_in(credentials)

            else:
                extended_credentials = ExtendedCredantialsDTO(user_id = user.user_id, email = user.email, username = user.username, new_user = False) 
                await self.create_access_token_response(user=extended_credentials)
                await login_context.execute_log_in(credentials)

        else:
            self._refresh_dal.revoke_all_refresh_and_access_tokens_for_user(user.user_id)


    async def __generate_auth_token(self, user, salt):
        return self._serializer.dumps(user.email, salt = salt)


    async def get_generate_auth_token(self, user):
        return await self.__generate_auth_token(user, salt = "user-auth-token")
    
    def __get_user_id_from_token(self):
        jwt = get_jwt()
        user_id = jwt.get('sub')
        return user_id

    def save_tokens_to_db(self, user, access_token: str, refresh_token: str):
        decode_access_token = decode_token(access_token)
        decode_refresh_token = decode_token(refresh_token)
        
        access_expires_at = datetime.utcfromtimestamp(decode_access_token['exp'])
        refresh_expires_at = datetime.utcfromtimestamp(decode_refresh_token['exp'])

        access_jwt_dto = JwtDTO(
            user_id=user.user_id,
            jti=decode_access_token[JTI],   
            token_type="access",
            revoked=False,
            expires_at=access_expires_at
        )
        self._access_tokens_dal.save_access_token(access_jwt_dto)

        refresh_jwt_dto = JwtDTO(
            user_id=user.user_id,
            jti=decode_refresh_token[JTI],
            token_type="refresh",
            revoked=False,
            expires_at=refresh_expires_at  
        )
        id = self._access_tokens_dal.save_access_token(refresh_jwt_dto)

        refresh_dto = RefreshTokenDTO(
            id=id,
            user_id=user.user_id,
            last_ip=self.__get_country_from_ip(),
            last_device=self.get_user_device(),
            nonce=self.generate_nonce()
        )
        self._refresh_dal.save_refresh_token(refresh_dto)
        # replace with the correct method user_id!!!


    async def create_access_token_response(self, user):
        additional_claims = AdditionalClaimsDTO(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            new_user=user.new_user
        )

        access_token = create_access_token(identity=user.email, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=user.email, additional_claims=additional_claims)

        self.save_tokens_to_db(user, access_token, refresh_token)
        
        result_data = ResponseDataDTO(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            new_user=user.new_user,
            access_token = access_token,
            refresh_token = refresh_token
        )

        response = jsonify(result_data.model_dump())
        response.set_cookie(
            "access_token",
            access_token,
            httponly=False,
            secure=True,
            samesite="None",
            path="/",
            max_age=3600
        )

        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=False,
            secure=True,
            samesite="None",
            path="/",
            max_age=30 * 24 * 3600
        )
        
        


    async def verify_nonce(self, user_email: str, token_nonce: str) -> bool:
        user = await self._user_dal.get_user_by_email(user_email)
        saved_nonce = self._refresh_dal.get_nonce_by_user_id(user.user_id)

        return saved_nonce == token_nonce


    async def update_refresh_token(self, user_email: str):
        user = await self._user_dal.get_user_by_email(user_email)
        
        refresh_dto = RefreshTokenDTO(
            user_id=user.user_id,
            last_ip=self.__get_country_from_ip(),
            last_device=self.get_user_device(),
            nonce=self.generate_nonce()
        )

        self._refresh_dal.update_refresh_token(user.user_id, refresh_dto)

    async def refresh_tokens(self):
        identity = get_jwt_identity()   
        current_refresh_token = get_jwt()

        token_nonce = current_refresh_token.get("nonce")

        if not self._refresh_dal.verify_nonce(identity, token_nonce):
            raise InvalidRefreshTokenError()

        new_access_token, new_refresh_token = await self.create_new_access_and_refresh_tokens(identity, refresh=True)

        new_nonce = self.generate_nonce()
        self._refresh_dal.update_refresh_token(identity, new_refresh_token, new_nonce)

        result = jsonify({
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        })

        
        response = jsonify(result.model_dump())
        response.set_cookie(
            "access_token",
            new_access_token,
            httponly=False,
            secure=True,
            samesite="None",
            path="/",
            max_age=3600
        )

        response.set_cookie(
            "refresh_token",
            new_refresh_token,
            httponly=False,
            secure=True,
            samesite="None",
            path="/",
            max_age=7 * 24 * 3600
        )
        

        

    
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
        if not dto.preferences:
            self._preferences_dal.delete_all_user_preferences(new_dto_by_type_of_preference, dto)
        else:
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
