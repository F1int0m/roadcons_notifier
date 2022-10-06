from enum import Enum


class UserRole(str, Enum):
    user = 'user'
    admin = 'admin'


class GoogleSheetEnums(str, Enum):
    kameralka = 'Камералка'
    podd = 'ПОДД'
    avtocad = 'Автокад'
