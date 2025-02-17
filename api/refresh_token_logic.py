from flask import request
from user_agents import parse
import requests

def get_user_device():
    user_agent = request.headers.get("User-Agent", "")
    parsed_agent = parse(user_agent)

    device_info = {
        "browser": f"{parsed_agent.browser.family} {parsed_agent.browser.version_string}",
        "os": f"{parsed_agent.os.family} {parsed_agent.os.version_string}",
        "device": parsed_agent.device.family
    }
    return f"{device_info['device']} | {device_info['os']} | {device_info['browser']}"


def get_client_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr)

def get_country():
    ip = get_client_ip()
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    return response.json().get("country")

# def is_ip_suspicious(old_ip, new_ip):
#     return get_country_from_ip(old_ip) != get_country_from_ip(new_ip)



# def is_suspicious_login(user_id, new_ip, new_device):
#     user = db.get_user(user_id)
    
#     if user.last_ip == new_ip or user.last_device == new_device:
#         return False 
#     return True
