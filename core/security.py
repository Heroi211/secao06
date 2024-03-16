from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'],deprecated="auto")

def verificaSenha(senha:str, hashSenha:str) -> bool:
    return CRIPTO.verify(senha,hashSenha)

def geraHashSenha(senha:str) ->str:
    return CRIPTO.hash(senha)

