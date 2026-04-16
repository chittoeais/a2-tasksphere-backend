from pydantic import BaseModel, EmailStr, field_validator

class UserRegister(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, v: str):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must be 72 bytes or fewer.")
        return v