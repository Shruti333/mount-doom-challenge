from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from ..api.models import ProcessedResult

class Database:
    def __init__(self, database_url):
        self.engine = create_async_engine(database_url)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        
    async def save_result(self, result: ProcessedResult):
        async with self.async_session() as session:
            session.add(result)
            await session.commit()