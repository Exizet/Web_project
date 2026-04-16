from fastapi import APIRouter, Depends, status, HTTPException, Request, Response, Cookie
from sqlalchemy import select, insert
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.gardener import Gardener
from app.models.snt import Snt
from app.schemas import CreateGardener
from app.Backend.db.db_depends import get_db

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix='/autorisation', tags=['auth'])
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

templates = Jinja2Templates(directory="app/Frontend/templates")
router.mount("/css", StaticFiles(directory="app/Frontend/css"), name="css")
router.mount("/src", StaticFiles(directory="app/Frontend/src"), name="src")

async def authenticate_user(db: Annotated[Session, Depends(get_db)], phone: str, password: str):
    user = db.scalar(select(Gardener).where(Gardener.phone == phone))
    if not user or not bcrypt_context.verify(password, user.hashed_password) or user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get('/')
async def get_auth_page(db: Annotated[Session, Depends(get_db)], request: Request):
    return templates.TemplateResponse("verificade.html", {'request': request})

@router.post('/')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateGardener):
    snt = db.scalar(select(Snt.id).where(Snt.name == create_user.snt, Snt.is_active==True))

    db.execute(insert(Gardener).values(
        name= create_user.name,
        phone= create_user.phone,
        email=create_user.email,
        hashed_password=bcrypt_context.hash(create_user.password),
        site_number=create_user.site_number,
        snt_id=snt
    ))
    db.commit()

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

SECRET_KEY = 'ed2846164bd6bfd62c80b4b08d0294562acb1f2c511a011d4fee8b507826885d'
ALGORITHM = "HS256"

async def create_access_token(username: str, user_id: int,snt_id: int, is_admin: bool, is_moderator: bool, is_user: bool, expires_delta: timedelta):
    payload = {
        'sub': username,
        'id': user_id,
        'snt_id': snt_id,
        'is_admin': is_admin,
        'is_moderator': is_moderator,
        'is_user': is_user,
        'exp': datetime.now(timezone.utc)+expires_delta
    }

    payload['exp'] = int(payload['exp'].timestamp())
    print('Create - good')
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/token")
async def login(db: Annotated[Session, Depends(get_db)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):
    user = await authenticate_user(db, form_data.username, form_data.password)

    token = await create_access_token(user.phone, user.id, user.snt_id, user.is_admin, user.is_moderator, user.is_user, expires_delta=timedelta(minutes=20))

    response.set_cookie(
        key="access_token",
        value=token,
        max_age=1200,  # 20 минут
        path="/",
        httponly=True,
        secure=False,  # Для разработки
        samesite="lax"
    )
    print('Login - good')
    print(token)
    return {
        'access_token': token,
        'token_type': 'bearer'
    }



async def get_current_user(request: Request, access_token: str| None = Cookie(None, alias='access_token')):
    token = access_token
    print(f'Token from cook {access_token}')
    if token is not None:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get('sub')
            user_id: int = payload.get('id')
            snt_id: int = payload.get('snt_id')
            is_admin: str = payload.get('is_admin')
            is_moderator: str = payload.get('is_moderator')
            is_user: str = payload.get('is_user')
            expire = payload.get('exp')
            if username is None or user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Could not validate user'
                )
            if expire is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No access token supplied"
                )
            if datetime.now() > datetime.fromtimestamp(expire):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token expired!"
                )
            return {
                'username': username,
                'id': user_id,
                'snt_id': snt_id,
                'is_admin': is_admin,
                'is_moderator': is_moderator,
                'is_user': is_user,
            }
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate user'
            )
    else:
        return {
            'username': None,
            'id': None,
            'snt_id': None,
            'is_admin': None,
            'is_moderator': None,
            'is_user': None,
        }
@router.get('/read_current_user')
async def read_current_user(user: dict = Depends(get_current_user)):
    return {'User' : user}