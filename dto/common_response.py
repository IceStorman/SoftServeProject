class CommonResponse:
    def __init__(self, message="Success"):
        self.message = message

    def __str__(self):
        return self.message

    def to_dict(self):
        return {"msg": self.message}


class CommonResponseWithUser:
    def __init__(self, message= "Bajojajo Bajojajo.You successfully logged in! Ya cie kurwa dam bajojajo bajojajo"):
        self.message = message
 
    def __str__(self):
        return f"{self.message}"

    def to_dict(self):
        return {"message": self.message, "login": True}
