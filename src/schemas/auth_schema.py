from pydantic import BaseModel
from pydantic.class_validators import validator, root_validator
from pydantic.fields import Field
from services.auth_service import AuthService


class AuthBase(BaseModel):
    username: str
    password: str = Field(min_length=8)

    @root_validator(pre=True)
    def hash_passwords(cls, values):
        password, password_repeat = values.get('password'), values.get('password_repeat')
        if password:
            cls.check_length_pass(password)
            values['password'] = AuthService.hash_password(password)
        if password_repeat:
            values['password_repeat'] = AuthService.hash_password(password_repeat)
        return values

    @staticmethod
    def check_length_pass(password):
        if len(password) < 8:
            raise ValueError('Пароль меньше 8 символов')


class LoginRequest(AuthBase):
    pass


class RegistrationRequest(AuthBase):
    password_repeat: str = Field(..., exclude=True)

    @validator('password_repeat')
    def passwords_match(cls, v, values):
        if v != values['password']:
            raise ValueError('Пароли не совпадают')
        return v
