from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import insert, select, update

from app.Backend.db.db_depends import get_db
from app.schemas import CreateContact
from app.models.snt import Snt
from app.models.contacts import Contacts

from app.routers.autorithation import get_current_user
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix='/governance', tags=['governance'])
templates = Jinja2Templates(directory="app/Frontend/templates")
router.mount("/css", StaticFiles(directory="app/Frontend/css"), name="css")
router.mount("/src", StaticFiles(directory="app/Frontend/src"), name="src")

@router.get('/')
async def get_contact_page(db: Annotated[Session, Depends(get_db)], request: Request, get_user = Depends(get_current_user)):
    if get_user.get('is_user'):
        snt = db.scalars(select(Snt).where(Snt.id == get_user.get('snt_id'), Snt.is_active == True)).all()
        contacts = db.scalars(select(Contacts).where(Contacts.snt_id == get_user.get('snt_id'), Contacts.is_active == True)).all()
        return templates.TemplateResponse("governance.html", {"request": request, "snt": snt[0], "contacts": contacts})
    else:
        return RedirectResponse('/autorisation/')

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_contact(db: Annotated[Session, Depends(get_db)], snt_id: int, create_contact: CreateContact):
    db.execute(insert(Contacts).values(
        name= create_contact.name,
        description= create_contact.description,
        time_contact= create_contact.time_contact,
        phone= create_contact.phone,
        email= create_contact.email,
        responsible= create_contact.responsible,
        title= create_contact.title,
        snt_id= snt_id
    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': "Succeful"
    }

@router.put('/{contact_id}')
async def update_contact(db: Annotated[Session, Depends(get_db)], snt_id: int, con_id: int, update_contact: CreateContact):
    contact = db.scalar(select(Contacts).where(Contacts.id == con_id, Contacts.snt_id== snt_id, Contacts.is_active==True))
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no SNT or contact ID"
        )
    db.execute(update(Contacts).where(Contacts.id == con_id, Contacts.snt_id==snt_id).values(
        name= update_contact.name,
        description = update_contact.description,
        time_contact=update_contact.time_contact,
        phone= update_contact.phone,
        email= update_contact.email,
        responsible= update_contact.responsible,
        title = update_contact.title
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': "Succeful update"
    }