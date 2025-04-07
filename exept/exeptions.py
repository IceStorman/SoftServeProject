class CustomQSportException(Exception):
    status_code = 400

    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)

    def get_response(self):
        return {"error": self.message}, self.status_code


class SportNotFoundError(CustomQSportException):
    status_code = 404

    def __init__(self, sport_name):
        self.sport_name = sport_name
        message = f"Sport '{sport_name}' not found"
        super().__init__(message)


class BlobFetchError(CustomQSportException):
    status_code = 401

    def __init__(self, blob_id):
        self.blob_id = blob_id
        message = f"Error while fetching blob data: '{blob_id}'"
        super().__init__(message)


class InvalidDateFormatError(CustomQSportException):
    status_code = 422

    def __init__(self, date_value):
        self.date_value = date_value
        message = f"Invalid date format: '{date_value}'"
        super().__init__(message)


class DatabaseConnectionError(CustomQSportException):
    status_code = 503

    def __init__(self, message="Database is currently unavailable. Please try again later."):
        super().__init__(message)


class InvalidResetPasswordError(CustomQSportException):
    status_code = 400

    def __init__(self, date_value):
        self.date_value = date_value
        message = f"Invalid or expired token'"
        super().__init__(message)


class UserDoesNotExistError(CustomQSportException):
    status_code = 404

    def __init__(self, date_value):
        self.date_value = date_value
        message = f"User '{date_value}' does not exist'"
        super().__init__(message)


class IncorrectUsernameOrEmailError(CustomQSportException):
    status_code = 401

    def __init__(self):
        message = f"Username or email are not correct'"
        super().__init__(message)


class IncorrectUserDataError(CustomQSportException):
    status_code = 401

    def __init__(self):
        message = f"Username/Email or password are not correct'"
        super().__init__(message)


class UserAlreadyExistError(CustomQSportException):
    status_code = 409

    def __init__(self):
        message = f"User with such data already exist'"
        super().__init__(message)


class IncorrectPreferencesError(CustomQSportException):
    status_code = 400

    def __init__(self):
        message = f"No valid preferences"
        super().__init__(message)


class IncorrectTypeOfPreferencesError(CustomQSportException):
    status_code = 400

    def __init__(self):
        message = f"Invalid preferences type"
        super().__init__(message)


class NoRecommendationListForUserError(CustomQSportException):
    status_code = 204

    def __init__(self, user_id):
        message = f"There are no recommendations for user '{user_id} at this moment'"
        super().__init__(message)


class IncorrectLogInStrategyError(CustomQSportException):
    status_code = 404

    def __init__(self, data_value):
        message = f"{data_value} is not a log in method in this app"
        super().__init__(message)


class InvalidAuthenticationDataError(CustomQSportException):
    status_code = 404

    def __init__(self, auth_provider_name):
        message = f"{auth_provider_name} data is invalid"
        super().__init__(message)

class IncorrectModelFromFilterManager(CustomQSportException):
    status_code = 404

    def __init__(self, table_name):
        message = f"No filter manager found for model: {table_name}"
        super().__init__(message)


class SignatureExpiredError(CustomQSportException):
    status_code = 401

    def __init__(self):
        message = f"Signature has expired"
        super().__init__(message)


class IncorrectSignatureError(CustomQSportException):
    status_code = 401

    def __init__(self):
        message = f"Incorrect type of signature"
        super().__init__(message)


class TokenRevokingError(CustomQSportException):
    status_code = 400

    def __init__(self):
        message = f"Cannot revoke token"
        super().__init__(message)

class TokenUpdatingError(CustomQSportException):
    status_code = 400

    def __init__(self):
        message = "Cannot update token"
        super().__init__(message)

class TokenSavingError(CustomQSportException):
    status_code = 400

    def __init__(self):
        message = "Cannot save token"
        super().__init__(message)
    
class InvalidRefreshTokenError(CustomQSportException):
    status_code = 400

    def __init__(self):
        message = "Invalid refresh token"
        super().__init__(message)

class ArticleNotFoundError(CustomQSportException):
    status_code = 404

    def __init__(self, blob_id):
        message = f"Article with blob_id {blob_id} not found"
        super().__init__(message)