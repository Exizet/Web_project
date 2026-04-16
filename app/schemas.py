from pydantic import BaseModel

class CreateSNT(BaseModel):
    name: str
    description: str
    all_sites: int
    free_sites: int | None = None

class CreateGardener(BaseModel):
    name: str
    phone: str
    password: str
    email: str
    snt: str
    site_number: int

class CreateAnnoncement(BaseModel):
    name: str
    description: str

class CreateContact(BaseModel):
    name: str
    description: str
    time_contact: str| None=None
    phone: str
    email: str
    responsible: str | None=None
    title: str

class CreatePhoto(BaseModel):
    name: str
    description: str | None=None

class CreateAlbum(BaseModel):
    name: str
    description: str | None=None
