from enum import Enum


class CommonConfig:
    def __init__(self) -> None:
        pass

    FONT_FAMILY = ("Roboto", 14)
    FONT_FAMILY_BOLD = ("Roboto", 14, 'bold')
    COMMON_FONT = ('Segoe UI', 11, 'bold')
    DEFAULT = ("Roboto", 14)


class Gender(Enum):
    FEMALE = 0
    MALE = 1
    OTHER = 2

class UserActive(Enum):
    INACTIVE = 0
    ACTIVE = 1

class UserType(Enum):
    ADMIN = 0
    NORMAL = 1

class Action(Enum):
    ADD = 0
    UPDATE = 1

