import requests

def get_country_from_ip(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    return response.json().get("country")

def is_ip_suspicious(old_ip, new_ip):
    return get_country_from_ip(old_ip) != get_country_from_ip(new_ip)

# def is_suspicious_login(user_id, new_ip, new_device):
#     user = db.get_user(user_id)
    
#     if user.last_ip == new_ip or user.last_device == new_device:
#         return False 
#     return True
