class SportNotFoundError(Exception):
    def __init__(self, sport_name):
        self.sport_name = sport_name
        self.message = f"Sport '{sport_name}' not found"
        super().__init__(self.message)


class BlobFetchError(Exception):
    def __init__(self, blob_id):
        self.blob_id = blob_id
        self.message = f"Error while fetching blob data: '{blob_id}'"
        super().__init__(self.message)


class InvalidDateFormatError(Exception):
    def __init__(self, date_value):
        self.date_value = date_value
        self.message = f"Invalid date format: '{date_value}'"
        super().__init__(self.message)


class DatabaseConnectionError(Exception):
    def __init__(self, message="Database is currently unavailable. Please try again later."):
        self.message = message
        super().__init__(self.message)





