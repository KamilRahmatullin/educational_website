from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from pydantic import BaseModel

from users.schemas import UserSchema
from auth import utils as auth_utils

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/demo-jwt-auth/login")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


demo_jwt_auth_router = APIRouter()

john = UserSchema(
    username='john',
    password=auth_utils.hash_password('qwerty'),
    email='john@example.com'
)

sam = UserSchema(
    username='sam',
    password=auth_utils.hash_password('qwerty123'),
    email='sam@example.com'
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail='Invalid username or password')
    if not (user := users_db.get(username)):
        raise unauthed_exc
    if not auth_utils.validate_password(password=password, hashed_password=user.password):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Inactive user'
        )
    return user


def get_current_token_payload(  # credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
        token: str = Depends(oauth2_scheme)
) -> UserSchema:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )
    return payload


def get_current_auth_user(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
    username: str | None = payload.get('sub')
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid token'
    )


def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Inactive user'
    )


@demo_jwt_auth_router.post('/login/', response_model=TokenInfo)
def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        # subject
        'sub': user.username,
        'username': user.username,
        'email': user.email
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type='Bearer'
    )


@demo_jwt_auth_router.get('/users/me/')
def auth_user_check_self_info(user: UserSchema = Depends(get_current_active_auth_user)):
    return {
        'username': user.username,
        'email': user.email,
    }
