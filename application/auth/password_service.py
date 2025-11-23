import bcrypt

class PasswordService:

    @staticmethod
    def _truncate(password: str) -> bytes:
        return password.encode("utf-8")[:72]   # bcrypt limit

    @staticmethod
    def hash_password(raw_password: str) -> str:
        truncated = PasswordService._truncate(raw_password)
        hashed = bcrypt.hashpw(truncated, bcrypt.gensalt())
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(raw_password: str, hashed_password: str) -> bool:
        truncated = PasswordService._truncate(raw_password)
        return bcrypt.checkpw(truncated, hashed_password.encode("utf-8"))
