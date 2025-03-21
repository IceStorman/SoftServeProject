from flask import request, jsonify, make_response
from database.postgres.dto.response_data import ResponseDataDTO
import requests
from flask_jwt_extended import get_jwt_identity, get_jwt
from exept.exeptions import InvalidRefreshTokenError
class RequestHelper():
    def __init__(self, user_service, access_tokens_dal, refresh_dal):
        self._user_service = user_service
        self._access_tokens_dal = access_tokens_dal
        self._refresh_dal = refresh_dal
        #Probilllllllllll
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
    
    def get_country_from_ip(self) -> str:
        return self.__get_country_from_ip()
    
    def create_responce(self, access_token, refresh_token,user):
        result_data = ResponseDataDTO(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            new_user=user.new_user,
            access_token = access_token.token,
            refresh_token = refresh_token.token
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
        
        return response
    
    
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
