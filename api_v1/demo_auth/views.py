import secrets
from time import time
import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials

demo_auth_router = APIRouter()

security = HTTPBasic()


@demo_auth_router.get('/basic-auth/')
def demo_basic_auth_credentials(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {
        'username': credentials.username,
        'password': credentials.password,
        'authenticated': True,
        'scope': ['read', 'write', 'delete']
    }


usernames_to_password = {
    'admin': 'admin',
    'user': '12345'
}

static_auth_token_to_username = {
    'a18b35d854726a2e128096ac2922a8c8': 'admin',
    '10b071e8d22f2d81c12fa010ac5eb9ca': 'john'
}


def get_username_by_static_auth_token(static_token: str = Header(alias='x-auth-token')) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


def get_auth_user_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials',
                                 headers={'WWW-Authenticate': 'Basic'})
    correct_password = usernames_to_password.get(credentials.username)
    if credentials.username not in usernames_to_password:
        raise unauthed_exc

    # secrets
    if not secrets.compare_digest(
            credentials.password.encode('utf-8'),
            correct_password.encode('utf-8')
    ):
        raise unauthed_exc

    return credentials.username


# basic authentication
@demo_auth_router.get('/basic-auth-username/')
def demo_basic_auth_credentials(auth_name: str = Depends(get_auth_user_username)):
    return {
        'message': f'Hi {auth_name}',
        'authenticated': True,
    }


@demo_auth_router.get('/some-http-header-auth/')
def demo_auth_some_http_header(username: str = Depends(get_username_by_static_auth_token)):
    return {
        'message': f'Hi {username}',
        'authenticated': True,
    }


COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = 'web-app-session-id'


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)):
    if session_id not in COOKIES:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')

    return COOKIES[session_id]


@demo_auth_router.post('/login-cookie/')
def demo_auth_login_cookie(response: Response, username: str = Depends(get_username_by_static_auth_token)):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        'username': username,
        'login_at': int(time())
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {'username': 'ok'}


@demo_auth_router.get('/check-cookie/')
def demo_auth_check_cookie(user_session_data: dict = Depends(get_session_data)):
    username = user_session_data['username']
    return {
        'username': username,
        **user_session_data
    }


@demo_auth_router.get('/logout-cookie/')
def demo_auth_logout_cookie(response: Response, session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
                            user_session_data: dict = Depends(get_session_data)):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data['username']
    return {
        'message': f'Bye, {username}!',
    }
