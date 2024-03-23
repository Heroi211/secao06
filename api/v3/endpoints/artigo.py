from typing import List
from fastapi import APIRouter,status,Depends,HTTPException,Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigo_model import ArtigoModel
from models.usuario_Model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema,ArtigoSchemaUpdate
from core.deps import get_session,getCurrentUser

router = APIRouter()

#post artigo
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=ArtigoSchema)
async def postArtigo(artigo: ArtigoSchema, UsuarioLogado: UsuarioModel = Depends(getCurrentUser), db: AsyncSession = Depends(get_session)):
    novoArtigo:ArtigoModel = ArtigoModel(
        titulo=artigo.titulo,
        descricao=artigo.descricao,
        url_fonte=artigo.url_fonte,
        usuario_id=UsuarioLogado.id, #independente do que estou mandando no body ele ta pegando o usuário autenticado pra enviar no post, por isso todos os artigos estão caindo com o mesmo ususario criado.
    )
    db.add(novoArtigo)
    await db.commit()
    return novoArtigo

#get artigos
@router.get('/',response_model=List[ArtigoSchema])
async def getArtigos(db:AsyncSession = Depends(get_session)):
    async with db as session:
        querie = select(ArtigoModel)
        result = await session.execute(querie)
        artigos: List[ArtigoModel] = result.scalars().unique().all()
        
        if artigos:
            return artigos
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Artigos não encontrados.')

#get artigo
@router.get('/{artigoID}',response_model=ArtigoSchema,status_code=status.HTTP_200_OK)
async def getArtigo(artigoID:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        querie = select(ArtigoModel).filter(ArtigoModel.id == artigoID)
        result = await session.execute(querie)
        artigo:ArtigoModel = result.scalars().unique().one_or_none()
        
        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Artigo não encontrado',status_code=status.HTTP_404_NOT_FOUND)

#put artigo
@router.put('/{artigoID}',response_model=ArtigoSchema,status_code=status.HTTP_202_ACCEPTED)
async def putArtigo(artigoID:int,artigo:ArtigoSchemaUpdate,db:AsyncSession = Depends(get_session),usuarioLogado:UsuarioModel=Depends(getCurrentUser)):
    async with db as session:
        querie = select(ArtigoModel).filter(ArtigoModel.id==artigoID)
        result = await session.execute(querie)
        artigoUP:ArtigoModel = result.scalars().unique().one_or_none()
        
        if artigoUP:
            if artigoUP.usuario_id == usuarioLogado.id:
                if artigo.titulo:
                    artigoUP.titulo = artigo.titulo
                if artigo.descricao:
                    artigoUP.descricao = artigo.descricao
                if artigo.url_fonte:
                    artigoUP.url_fonte = artigo.url_fonte
                if usuarioLogado.id != artigoUP.usuario_id:
                    artigoUP.usuario_id = usuarioLogado.id
                await session.commit()
                return artigoUP
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Artigo ainda não liberado para reviews públicas.')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Artigo não encontrado.')
            
#delete artigo
@router.delete ('/{artigoID}',status_code=status.HTTP_204_NO_CONTENT)
async def deleteArtigo(artigoID:int,db:AsyncSession=Depends(get_session),usuarioLogado:UsuarioModel = Depends(getCurrentUser)):
    async with db as session:
        querie = select(ArtigoModel).filter(ArtigoModel.id==artigoID)#.filter(ArtigoModel.usuario_id == usuarioLogado.id)
        result = await session.execute(querie)
        artigoDel:ArtigoModel = result.scalars().unique().one_or_none()
        
        if artigoDel:
            if usuarioLogado.id == artigoDel.usuario_id:
                await session.delete(artigoDel)
                await session.commit()
            
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Apenas o criador do artigo pode excluir o trabalho.')
        else:
            raise HTTPException(detail='Artigo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)