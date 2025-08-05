from sqlalchemy import Column, Integer, BigInteger, Boolean, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()
database_url = 'sqlite+aiosqlite:///users.db'
engine = create_async_engine(database_url)
AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)

    is_active = Column(Boolean, nullable=False, default=False)
    last_message_id = Column(Integer, nullable=True)
    is_uploading_photo = Column(Boolean, nullable=False, default=False)
    gender = Column(String, nullable=False, default='male')
    template_id = Column(Integer, nullable=True)
    last_photo_id = Column(String, nullable=True)
    generation_count = Column(Integer, nullable=False, default=0)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
