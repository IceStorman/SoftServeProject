class CommonResponse:
    def __init__(self, message="Success"):
        self.message = message

    def __str__(self):
        return self.message

    def to_dict(self):
        return {"msg": self.message}


class CommonResponseWithUser:
    def __init__(self, user_id: int, user_email: str, message= "You successfully logged in!"):
        self.message = message
        self.user = {"id": user_id, "email": user_email}

    def __str__(self):
        return f"{self.message}, User: {self.user}"

    def to_dict(self):
        return {"message": self.message, "user": self.user, "login": True}
