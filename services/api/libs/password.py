import bcrypt


class Password:
    """
    Class to create a hashed password where the orignal password is not accessible.
    """
    def __init__(self) -> None:
        self._password = ""

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password) -> None:
        """
        Method to set password attribute to a hashed value.
        Args:
            password: string value to be hashed
        """
        self._password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    @staticmethod
    def check_password(password, hashed_password) -> bool:
        """
        Validates password against the expected hashed value.

        Args:
            password: string to be validated
            hashed_password: expected hashed value
        Returns:
            True if password is valid. False otherwise.
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


if __name__ == "__main__":
    pword = Password()
    pword.password = "Pa$sW0rd123"
    print("Hashed Password: ", pword.password)
    print("Validate Incorrect Password: ", pword.check_password("WrongPassword", pword.password))
    print("Validate Correct Password: ", Password.check_password("Pa$sW0rd123", pword.password))
