class Error(Exception):
    """Base class for other exceptions in the game"""
    pass

class InvalidFormatError(Error):
    """Raised when the player input is not in the right format"""
    pass

class PositionOccupiedError(Error):
    """Raised when a ship cannot fit the board"""
    pass

class ShipOverlapError(Error):
    """Raised when a ship overlaps with another"""
    pass
