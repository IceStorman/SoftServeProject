from flask import request
from user_agents import parse
import requests
import hashlib
import time
import os

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

def generate_nonce():
    nonce = hashlib.sha256(f"{time.time()}{os.urandom(16)}".encode()).hexdigest()
    return nonce


# def is_ip_suspicious(old_ip, new_ip):
#     return get_country_from_ip(old_ip) != get_country_from_ip(new_ip)



