"""
SearchOption enum class
"""

from enum import IntEnum


class SearchOption:
    class Broadcast(Enum):
        BS = 1
        CS = 2
        TERRESTRIAL = 3

        def __str__(self):
            return str(self.value)

    class Prefecture(Enum):
        SAPPORO = 10
        HAKODATE = 11
        ASAHIKAWA = 12
        OBIHIRO = 13
        KUSHIRO = 14
        KITAMI = 15
        MURORAN = 16
        AOMORI = 22
        IWATE = 20
        MIYAGI = 17
        AKITA = 18
        YAMAGATA = 19
        FUKUSHIMA = 21
        TOKYO = 23
        KANAGAWA = 24
        SAITAMA = 29
        CHIBA = 27
        IBARAKI = 26
        TOCHIGI = 28
        GUNMA = 25
        YAMANASHI = 32
        NIIGATA = 31
        NAGANO = 30
        TOYAMA = 37
        ISHIKAWA = 34
        FUKUI = 36
        AICHI = 33
        GIFU = 39
        SHIZUOKA = 35
        MIE = 38
        OSAKA = 40
        HYOUGO = 42
        KYOTO = 41
        SHIGA = 45
        NARA = 44
        WAKAYAMA = 43
        TOTTORI = 49
        SHIMANE = 48
        OKAYAMA = 47
        HIROSHIMA = 46
        YAMAGUCHI = 50
        TOKUSHIMA = 53
        KAGAWA = 52
        EHIME = 51
        KOCHI = 54
        FUKUOKA = 55
        SAGA = 61
        NAGASAKI = 57
        KUMAMOTO = 56
        OITA = 60
        MIYAZAKI = 59
        KAGOSHIMA = 58
        OKINAWA = 62

        def __str__(self):
            return str(self.value)
