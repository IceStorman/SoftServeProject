from flask import request, jsonify
from user_agents import parse
import requests
from dto.api_output import OutputLogin


class RequestHelper():
    @staticmethod    
    def get_user_device() -> str:
        user_agent = request.headers.get("User-Agent", "")
        parsed_agent = parse(user_agent)
        device_info_str = f"Browser: {parsed_agent.browser.family} {parsed_agent.browser.version_string}, " \
                        f"OS: {parsed_agent.os.family} {parsed_agent.os.version_string}, " \
                        f"Device: {parsed_agent.device.family}"
        
        return device_info_str 
      
    @staticmethod      
    def get_client_ip() -> str:
        return request.headers.get("X-Forwarded-For", request.remote_addr)

    @staticmethod 
    def get_country_from_ip() -> str:
        ip = RequestHelper.get_client_ip()

        try:
            country = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
            country.raise_for_status()
            unknown = "Unknown"
            
            return country.json().get("country", unknown)
        
        except (requests.RequestException, ValueError):
            return unknown
    

    @staticmethod
    async def set_tokens_and_create_response(user: OutputLogin):
        result_data = {
            "user_id": user.user_id,
            "email": user.email,
            "username": user.username,
            "new_user": user.new_user,
            "access_token": user.access_token,
            "refresh_token": user.refresh_token,
            "message": user.message
        }
        
        response = jsonify(result_data)
        response.set_cookie(
            "access_token",
            user.access_token,
            httponly=False,
            secure=True,
            samesite="None",
            path="/",
            max_age=3600
        )
        
        response.set_cookie(
            "refresh_token_cookie",
            user.refresh_token,
            httponly=False,
            secure=True,
            samesite="None",
            path="/",
            max_age=30 * 24 * 3600
        )
        
        return response
    