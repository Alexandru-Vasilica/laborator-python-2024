class RESPException(Exception):
    """
    Exception related to the connection to a Redis server
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
