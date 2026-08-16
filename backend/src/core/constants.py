import string


class CharacterSet:

    LOWERCASE = list(string.ascii_lowercase)
    UPPERCASE = list(string.ascii_uppercase)
    DIGITS = list(string.digits)
    PUNCTUATION = list(string.punctuation)

    ARABIC_LETTERS = [chr(i) for i in range(0x0621, 0x064B)]
    ARABIC_TASHKEEL = [chr(i) for i in range(0x064B, 0x0653)]

    RUSSIAN = [chr(i) for i in range(0x0410, 0x0450)]
    ABUGIDAS = [chr(i) for i in range(0x0905, 0x093A)]
    SYLLABARIES = [chr(i) for i in range(0x3041, 0x3097)] 
    KATAKANA = [chr(i) for i in range(0x30A1, 0x30FB)]
    CHEROKEE = [chr(i) for i in range(0x13A0, 0x13F6)]

    @classmethod
    def get_all(
        cls,
        include_numbers: bool = True,
        include_alphabit: bool = True,
        include_punctuation: bool = True,
        include_arabic: bool = True,
        include_russian: bool = True,
        include_abugidas: bool = True,
        include_katakana: bool = True,
        include_cherokee: bool = True,
    ):
        chars = []

        if include_alphabit:
            chars += cls.LOWERCASE + cls.UPPERCASE

        if include_numbers:
            chars += cls.DIGITS

        if include_punctuation:
            chars += cls.PUNCTUATION

        if include_arabic:
            chars += cls.ARABIC_LETTERS + cls.ARABIC_TASHKEEL

        if include_russian:
            chars += cls.RUSSIAN

        if include_abugidas:
            chars += cls.ABUGIDAS

        if include_katakana:
            chars += cls.KATAKANA

        if include_cherokee:
            chars += cls.CHEROKEE

        return chars