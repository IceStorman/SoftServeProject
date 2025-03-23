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
    
    async def create_response(self, access_token, refresh_token, user):
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
            "refresh_token_cookie",
            refresh_token,
            httponly=False,
            secure=True,
            samesite="None",
            path="/",
            max_age=30 * 24 * 3600
        )
        
        return response