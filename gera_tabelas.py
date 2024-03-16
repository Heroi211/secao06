from core.configs import settings
from core.database import engine

from dotenv import load_dotenv

load_dotenv()

async def createTables() ->None:
    import models.__all_models
    print("criandos as tabelas nas base myfriend")
    async with engine.begin() as connection:
        await connection.run_sync(settings.DBBaseModel.metadata.drop_all)
        await connection.run_sync(settings.DBBaseModel.metadata.create_all)
    print("Tabelas criadas myfriend")
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(createTables())