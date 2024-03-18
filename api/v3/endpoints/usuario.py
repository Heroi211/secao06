from typing import List,Optional,Any

from fastapi import APIRouter,status,Depends,HTTPException,Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_Model import UsuarioModel
from schemas.usuario_schema import UsuarioSchema,UsuarioSchemaCreate,UsuarioSchemaUp

from core.deps import get_session,getCurrentUser
from core.security import geraHashSenha
from core.auth import autenticar,criar_token_acesso

router = APIRouter()

#get logado
@router.get('/logado',response_model=UsuarioSchema)
def get_logado(usuario_logado: UsuarioModel = Depends(getCurrentUser)):
    return usuario_logado

#POST /SingUP
@router.post('/signup',response_model=UsuarioSchema,status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioSchemaCreate,db:AsyncSession=Depends(get_session)):
    novoUsuario:UsuarioModel=UsuarioModel(nome=usuario.nome,sobrenome=usuario.sobrenome,
                                          email=usuario.email,
                                          senha=geraHashSenha(usuario.senha),eh_admin=usuario.eh_admin)
    async with db as session:
        session.add(novoUsuario)
        session.commit()
        
        return novoUsuario
    
#GET Usuarios
@router.get('/',response_model=UsuarioSchema)
async def get_usuarios(db:AsyncSession=Depends(get_session)):
    async with db as session:
        querie = select(UsuarioModel)
        result = await session.execute(querie)
        Usuarios:List[UsuarioSchema]=result.scalars().unique().all()
        
        return Usuarios
    
#GET Usuario
@router.get('/{usuario_id}',response_model=UsuarioSchema)
async def get_usuario(usuario_id:int,db:AsyncSession=Depends(get_session)):
    async with db as session:
        querie = select(UsuarioModel).filter(UsuarioModel.id==usuario_id)
        result = await session.execute(querie)
        usuario = result.scalars().unique().one_or_none()
    
    if usuario:
        return usuario
    else:
        raise HTTPException(detail='Usuário não encontrado',
                            status_code=status.HTTP_404_NOT_FOUND)

#PUT usuario
@router.put('/{usuario_id}', response_model=status.HTTP_201_CREATED)
async def put_usuario(usuario_id:int,usuario:UsuarioSchemaUp,db:AsyncSession=Depends(get_session)):
    async with db as session:
        querie = select(UsuarioModel).filter(UsuarioModel.id==usuario_id)
        result = await session.execute(querie)
        usuarioUP:UsuarioSchema=result.scalars().unique().one_or_none()
    
    if usuarioUP:
        if usuario.id:
            usuarioUP.id = usuario.id
        if usuario.nome:
            usuarioUP.nome = usuario.nome    
        if usuario.sobrenome:
            usuarioUP.sobrenome = usuario.sobrenome
        if usuario.email:
            usuarioUP.email = usuario.email
        if usuario.senha:
            usuarioUP.senha = geraHashSenha(usuario.senha)
        if usuario.eh_admin:
            usuarioUP.eh_admin = usuario.eh_admin
        await session.commit()
    else:
        raise HTTPException(detail='Usuário não encontrado.',
                           status_code=status.HTTP_404_NOT_FOUND)
        
#DELETE usuario
@router.delete('/{usuario_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id:int,db:AsyncSession=Depends(get_session)):
    async with db as session:
        querie = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(querie)
        usuariodel = result.scalars().unique().one_or_none()
        
    if usuariodel:
        session.delete(usuariodel)
        session.commit()
        
        return(status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(detail='Usuário não encotrado.',
                            status_code=status.HTTP_404_NOT_FOUND)
        

#POST login
@router.post('/login')
async def login_usuario(form_data: OAuth2PasswordRequestForm=Depends(),db:AsyncSession=Depends(get_session())):
    usuario = await autenticar(email=form_data.username,senha=form_data.password,db=db)
    
    if not usuario:
        raise HTTPException(detail='Login não autorizado ou dados incorretos',
                            status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id),"token_type":"bearer"},status_code=status.HTTP_200_OK)        
        

