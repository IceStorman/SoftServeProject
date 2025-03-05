from flask import request
from user_agents import parse
import requests
import hashlib
import time
import os
from typing import Optional

class UserInfo:
    def get_user_device(self) -> str:
        user_agent = request.headers.get("User-Agent", "")
        parsed_agent = parse(user_agent)

        device_info = {
            "browser": f"{parsed_agent.browser.family} {parsed_agent.browser.version_string}",
            "os": f"{parsed_agent.os.family} {parsed_agent.os.version_string}",
            "device": parsed_agent.device.family
        }
        return f"{device_info['device']} | {device_info['os']} | {device_info['browser']}"


    def get_client_ip(self) -> str:
        return request.headers.get("X-Forwarded-For", request.remote_addr)

    def get_country_from_ip(self) -> str:
        ip = self.get_client_ip()
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
            response.raise_for_status()
            return response.json().get("country", "Unknown")
        except (requests.RequestException, ValueError):
            return "Unknown"

    def is_ip_country_changed(self, stored_country: str) -> bool:
        current_country = self.get_country_from_ip()
        return stored_country != current_country

    def is_device_changed(self, stored_device: str) -> bool:
        current_device = self.get_user_device()
        return stored_device != current_device

    def generate_nonce(self):
        nonce = hashlib.sha256(f"{time.time()}{os.urandom(16)}".encode()).hexdigest()
        return nonce
    
    def is_suspicious_login(self):
        pass





# def is_ip_suspicious(old_ip, new_ip):
#     return get_country_from_ip(old_ip) != get_country_from_ip(new_ip)



