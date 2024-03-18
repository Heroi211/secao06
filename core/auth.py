from pytz import timezone

from typing import Optional,List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.usuario_Model import UsuarioModel
from core.configs import settings
from core.security import verificaSenha
from pydantic.v1 import EmailStr

oauth2Schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V3_VERSION}/usuarios/login"
)

async def autenticar(email: EmailStr,senha:str, db: AsyncSession)-> Optional[UsuarioModel]:
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario = UsuarioModel = result.scalars().unique().one_or_none()
        
        if not usuario:
            return None
        
        if not verificaSenha(senha,usuario.senha):
            return None
        
        return usuario
        
def _criar_token(tipo_token:str,tempoVida:timedelta,sub:str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    payload = {}
    
    sp = timezone('america/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempoVida
    
    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)
    
    return jwt.encode(payload,settings.JWT_SECRET,algorithm=settings.ALGORITH)

def criar_token_acesso(sub:str) -> str:
    """
        http://jwt.io
    """
    return _criar_token(
        tipo_token='access_token',
        tempoVida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
