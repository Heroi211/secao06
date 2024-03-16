from typing import Generator, Optional

from fastapi import Depends,HTTPException,status
from jose import jwt,JWTError


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from pydantic.v1 import BaseModel
from core.database import Session
from core.auth import oauth2Schema
from core.configs import settings
from models.usuario_Model import UsuarioModel

class TokenData(BaseModel):
    username: Optional[str]= None


async def get_session() -> Generator:  # type: ignore
    session: AsyncSession = Session()
    
    try:
        yield Session
    finally:
        await Session.close()
        
async def getCurrentUser(db: Session = Depends(get_session),token: str = Depends(oauth2Schema)) -> UsuarioModel:
    credentialException: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível autenticar a credencial',
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITH],
            options={"verify_aud":False}
        )
        username:str = payload.get("sub")
        if username is None:
            raise credentialException
        token_data :TokenData = TokenData(username = username)
    except JWTError:
        raise credentialException
    
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == int(token_data.username) )
        result = await session.execute(query)
        usuario:UsuarioModel = result.scalars().unique().one_or_None()
        
        if usuario is None:
            raise credentialException
        
        return usuario
        
        