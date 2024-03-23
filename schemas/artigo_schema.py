from typing import Optional
from pydantic import BaseModel as BaseModelSchema

class ArtigoSchema(BaseModelSchema):
    id:Optional[int] = None
    titulo: str
    descricao: str
    url_fonte: str
    usuario_id: Optional[int]
    
    class Config:
        orm_mode = True

class ArtigoSchemaUpdate(ArtigoSchema):
    id:Optional[int] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    url_fonte: Optional[str] = None
    usuario_id: Optional[int] = None
    
        
        