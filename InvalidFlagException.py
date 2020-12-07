# file created by Sheldon Dorgelo
# custom exception for an invalid flag in DataProcessor

class InvalidFlagException(Exception):
    def __init__(self, error):
        print(error)