
def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def print_error_message(message):
    red_text = color_text(message, "31")
    print(red_text)

def print_good_message(message):
    red_text = color_text(message, "32")
    print(red_text)

