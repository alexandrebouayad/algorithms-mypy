def _ord(char: str) -> int:
    return ord(char) - ord("A")


def _chr(code: int) -> str:
    return chr(code + ord("A"))


def _transform(message: str, shift: int) -> str:
    shifted_message = [
        _chr((_ord(char) + shift) % 26) if char.isupper() else char
        for char in message
    ]
    return "".join(shifted_message)


class CaesarCipher:
    """
    Encryption and decryption using a Caesar cipher.

    >>> cipher = CaesarCipher(3)
    >>> message = "THE EAGLE IS IN PLAY; MEET AT JOE'S."
    >>> cypher_test = cipher.encrypt(message)
    >>> cypher_test
    "WKH HDJOH LV LQ SODB; PHHW DW MRH'V."
    >>> cipher.decrypt(cypher_test)
    "THE EAGLE IS IN PLAY; MEET AT JOE'S."
    """

    def __init__(self, shift: int) -> None:
        """Create Caesar cipher using given integer shift for rotation."""
        self.shift = shift

    def encrypt(self, message: str) -> str:
        """Return encripted message."""
        return _transform(message, self.shift)

    def decrypt(self, message: str) -> str:
        """Return decrypted message."""
        return _transform(message, -self.shift)
