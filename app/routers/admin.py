from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from app.Backend.db.db_depends import get_db
from app.schemas import CreateSNT
from app.models.snt import Snt
from app.routers.autorithation import get_current_user

router = APIRouter(prefix='/admin', tags=['admin'])

templates = Jinja2Templates(directory="app/Frontend/templates")
router.mount("/css", StaticFiles(directory="app/Frontend/css"), name="css")
router.mount("/src", StaticFiles(directory="app/Frontend/src"), name="src")

@router.get('/')
async def get_admin_page(db: Annotated[Session, Depends(get_db)], request: Request, get_user = Depends(get_current_user)):
    if get_user.get('is_moderator'):

