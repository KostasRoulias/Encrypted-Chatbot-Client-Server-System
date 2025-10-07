class vignere_cipher:
    """ vignere_cipher
        Handles encryption of upper, lower, numeric, and symbols within their own ranges (e.g. upper->upper)
        """
    # The set_key method initializes the encryption key,
    # and the encrypt and decrypt methods apply the Vigenère cipher
    # to the input message, preserving the case and characteristics of
    # different character ranges (uppercase letters, lowercase letters, digits, and symbols)

    def __init__(self):
        self.key = ""
        self.key_length = 0
        self.offsets = list()

    def set_key(self, key) -> bool:
        self.key = key
        self.key_length = len(self.key)
        for character in self.key:
            self.offsets.append(int(ord(character)))
        return True

    def encrypt(self, message) -> str:
        if self.key_length == 0:
            return message

        output_list = list()
        wrap = 0
        bias = 0

        for i in range(len(message)):
            offset = self.offsets[i%self.key_length]
            ordinal_value = ord(message[i])

            if ordinal_value == 63:  # Question mark
                output_list.append("?")
                continue
            if ordinal_value >= 65 and ordinal_value <= 90:  # Uppercase letters
                bias = 65
                wrap = 26
            elif ordinal_value >= 97 and ordinal_value <= 122:  # Lowercase letters
                bias = 97
                wrap = 26
            elif ordinal_value >= 48 and ordinal_value <= 57:  # Digits
                bias = 48
                wrap = 10
            elif ordinal_value >= 32 and ordinal_value <= 47:  # Symbols
                bias = 32
                wrap = 15
            else:
                bias = 0
                wrap = ordinal_value+1

            zero_biased = ordinal_value - bias
            wrapped = (zero_biased + offset) % wrap
            rebiased = wrapped + bias

            output_list.append(chr(rebiased))

        encrypted = "".join(output_list)
        return encrypted


    def decrypt(self, message) -> str:
        if self.key_length == 0:
            return message

        output_list = list()
        wrap = 0
        bias = 0

        for i in range(len(message)):
            offset = self.offsets[i % self.key_length]
            ordinal_value = ord(message[i])

            if ordinal_value == 63:  # Question mark
                output_list.append("?")
                continue

            if ordinal_value >= 65 and ordinal_value <= 90:  # Uppercase letters
                bias = 65
                wrap = 26
            elif ordinal_value >= 97 and ordinal_value <= 122:  # Lowercase letters
                bias = 97
                wrap = 26
            elif ordinal_value >= 48 and ordinal_value <= 57:  # Digits
                bias = 48
                wrap = 10
            elif ordinal_value >= 32 and ordinal_value <= 47:  # Symbols
                bias = 32
                wrap = 15
            else:
                bias = 0
                wrap = ordinal_value + 1

            zero_biased = ordinal_value - bias
            wrapped = (zero_biased - offset) % wrap
            rebiased = wrapped + bias

            output_list.append(chr(rebiased))

        decrypted = "".join(output_list)
        return decrypted

# Create an instance of the class
crypto = vignere_cipher()

message = ""
key = "DerbyUniversity"
crypto.set_key(key)
encrypted = crypto.encrypt(message)
decrypted = crypto.decrypt(encrypted)

