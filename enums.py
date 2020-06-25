from enum import Enum


class CustomEnum(Enum):
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class RolesType(CustomEnum):
    ADMINISTRATOR = 'Администратор'


class ColorsType(CustomEnum):
    DEFAULT = 0x55c025
    ERROR = 0xe31e2f
    WARNING = 0xf2d823
