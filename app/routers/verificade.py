from fastapi import APIRouter, Depends, status, HTTPException, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from sqlalchemy import insert, select, update
from fastapi.responses import HTMLResponse, RedirectResponse
import os
from transliterate import translit, get_available_language_codes

from app.Backend.db.db_depends import get_db
from app.schemas import CreatePhoto, CreateAlbum
from app.routers.autorithation import get_current_user
from app.models.snt import Snt
from app.models.photo import Photo
from app.models.album import Album
from app.models.gardener import Gardener
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix='/verificade', tags=['verificade'])
templates = Jinja2Templates(directory="app/Frontend/templates")

router.mount("/css", StaticFiles(directory="app/Frontend/css"), name="css")
router.mount("/src", StaticFiles(directory="app/Frontend/src"), name="src")

@router.get('/')
async def get_personal_page(db: Annotated[Session, Depends(get_db)],request: Request, get_user = Depends(get_current_user) ):
    if get_user.get('is_user'):
        gardener = db.scalars(select(Gardener).where(Gardener.id == get_user.get("id"), Gardener.is_active == True)).all()
        snt = db.scalars(select(Snt).where(Snt.id == get_user.get('snt_id'), Snt.is_active == True)).all()
        return templates.TemplateResponse('PersonalAccaunt.html', {"request": request, 'snt': snt[0], 'user': gardener[0]})
    else:
        pass
