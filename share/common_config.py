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

class UserStatus(Enum):
    INACTIVE = 0
    ACTIVE = 1

class UserType(Enum):
    ADMIN = 0
    NORMAL = 1

class Action(Enum):
    ADD = 0
    UPDATE = 1
    DELETE = 2

class Tab(Enum):
    EMPLOYEE = 0
    TABLE = 1
    INVOICE = 2
    WARE_HOUSE = 3
    REPORT = 4
    LOG_OUT = 5

class TabType(Enum):
    EMPLOYEE = "EMPLOYEE"
    TABLE = "TABLE"
    BILL = "BILL"
    REPORT = "REPORT"
    LOGOUT = "LOGOUT"
    WARE_HOUSE = "WARE_HOUSE"

class StatusTable(Enum):
    DISABLED = "Đã đặt"
    AVAILABLE = "Trống"
