class SteamingException(Exception):
    """
    Default exception
    """

class MovieNotFoundException(SteamingException):
    """
    Movie not found
    """

class NoPosterException(SteamingException):
    """
    Movie has no poster
    """