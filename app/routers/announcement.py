from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import insert, select, update

from app.Backend.db.db_depends import get_db
from app.schemas import CreateAnnoncement
from app.models.snt import Snt
from app.routers.autorithation import get_current_user
from app.models.announcement import Announcement
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix='/announcement', tags=['announcement'])
templates = Jinja2Templates(directory="app/Frontend/templates")
router.mount("/css", StaticFiles(directory="app/Frontend/css"), name="css")
router.mount("/src", StaticFiles(directory="app/Frontend/src"), name="src")


@router.get('/')
async def get_announcement_page(db: Annotated[Session, Depends(get_db)], request: Request, get_user = Depends(get_current_user)):
    if get_user.get('is_user'):
        snt = db.scalars(select(Snt).where(Snt.id == get_user.get('snt_id'), Snt.is_active==True)).all()
        announcement = db.scalars(select(Announcement).where(Announcement.snt_id == get_user.get('snt_id'), Announcement.is_active == True)).all()
        return templates.TemplateResponse("announcement.html", {"request": request, "snt": snt[0], "announcement": announcement})
    else:
        return RedirectResponse('/autorisation/')

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_announcement(db: Annotated[Session, Depends(get_db)], create_announce: CreateAnnoncement, snt_id: int):
    db.execute(insert(Announcement).values(
        name= create_announce.name,
        description= create_announce.description,
        snt_id= snt_id
    ))
    db.commit()
    return{
        'status_code': status.HTTP_201_CREATED,
        'transaction': "Succeful"
    }
@router.put('/{announce_id}')
async def update_announcement(db: Annotated[Session, Depends(get_db)], update_announce: CreateAnnoncement, snt_id: int, announce_id: int):
    announce = db.scalar(select(Announcement).where(Announcement.id == announce_id, Announcement.snt_id==snt_id, Announcement.is_active==True))
    if announce is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no SNT or Announce ID"
        )
    db.execute(update(Announcement).where(Announcement.id == announce_id, Announcement.snt_id == snt_id).values(
        name= update_announce.name,
        description= update_announce.description
    ))
    db.commit()
    return{
        'status_code': status.HTTP_200_OK,
        'transaction': "Succeful update"
    }