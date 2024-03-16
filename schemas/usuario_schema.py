from typing import Optional, List
from pydantic import BaseModel as BaseModelSchema, EmailStr
from schemas.artigo_schema import ArtigoSchema

class UsuarioSchema(BaseModelSchema):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False
    
    class Config:
        orm_mode = True

class UsuarioSchemaCreate(UsuarioSchema):
    senha:str
    
class UsuarioSchemaArtigos(UsuarioSchema):
    artigos: Optional[List[ArtigoSchema]]
    
class UsuarioSchemaUp(UsuarioSchema):
    nome: Optional[str]
    sobrenome: Optional[str]
    email:Optional[EmailStr]
    senha:Optional[str]
    eh_admin:Optional[bool]