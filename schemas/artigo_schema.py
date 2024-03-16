from typing import Optional
from pydantic import BaseModel as BaseModelSchema, HttpUrl

class ArtigoSchema(BaseModelSchema):
    id:Optional[int] = None
    titulo: str
    descricao: str
    url_fonte: HttpUrl
    usuario_id: Optional[int]
    
    class Config:
        orm_mode = True
        
        