import string


class CharacterSet:
    LOWERCASE = list(string.ascii_lowercase)
    UPPERCASE = list(string.ascii_uppercase)
    DIGITS = list(string.digits)
    PUNCTUATION = list(string.punctuation)
    ARABIC_LETTERS = [chr(i) for i in range(0x0621, 0x064B)]
    ARABIC_TASHKEEL = [chr(i) for i in range(0x064B, 0x0653)]

    @classmethod
    def get_all(cls,include_arabic: bool = False):
        chars = cls.LOWERCASE + cls.UPPERCASE + cls.DIGITS + cls.PUNCTUATION
        if include_arabic:
            chars += cls.ARABIC_LETTERS + cls.ARABIC_TASHKEEL
        return chars