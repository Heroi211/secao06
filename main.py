from fastapi import FastAPI

from core.configs import settings
from api.v3.api import api_router

app = FastAPI(title='Curso API - Security')
app.include_router(api_router,prefix=settings.API_V3_VERSION)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",host="0.0.0.0",
                port=8000,reload=True)
    
    