from typing import AsyncGenerator, Sequence

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import (Column, ForeignKey, Integer, Table,
                        orm, select)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (AsyncAttrs, AsyncSession,
                                    async_sessionmaker, create_async_engine)

# %%%%%%%%%%%%%%%%%%%%%%%
# core.py

# Globals
DATABASE_URL = "sqlite+aiosqlite:///./app.db"
ENGINE = create_async_engine(DATABASE_URL, echo=True, future=True,
                            connect_args={"check_same_thread": False}  # Only for SQLite
                            )
SESSION_FACTORY = async_sessionmaker(ENGINE, expire_on_commit=False, class_=AsyncSession)

# %%%%%%%%%%%%%%%%%%%%%%%
# models.py


class AlchemyAsyncBase(orm.DeclarativeBase, AsyncAttrs):
    pass


METADATA = AlchemyAsyncBase.metadata  # Use this metadata in migrations


association_table = Table(
    "item_tag",
    METADATA,
    Column("item_id", Integer, ForeignKey("item.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class Item(AlchemyAsyncBase):
    __tablename__ = "item"
    # Regular attributes
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    title: orm.Mapped[str] = orm.mapped_column(nullable=True)
    url: orm.Mapped[str] = orm.mapped_column()
    counter: orm.Mapped[int] = orm.mapped_column(default=0)
    # Relationships
    tags: orm.Mapped[list["Tag"]] = orm.relationship(secondary=association_table, back_populates="items")


class Tag(AlchemyAsyncBase):
    __tablename__ = "tag"
    # Regular attributes
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str]
    # Relationships
    items: orm.Mapped[list[Item]] = orm.relationship(secondary=association_table, back_populates="tags")


# %%%%%%%%%%%%%%%%%%%%%%%
# schemas.py
# Pydantic schemas


class PyItemBase(BaseModel):
    title: str | None
    url: str
    counter: int

    class Config:
        orm_mode = True


class PyItemIn(PyItemBase):
    tag_names: list[str] = Field(default_factory=list)


class PyItemOutMinimal(PyItemBase):  # Minimal classes are used to avoid infinite recursion
    id: int


class PyItemOut(PyItemOutMinimal):
    tags: list["PyTagOutMinimal"]


class PyTagBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class PyTagIn(PyTagBase):
    pass


class PyTagOutMinimal(PyTagBase):
    id: int


class PyTagOut(PyTagOutMinimal):
    items: list["PyItemOutMinimal"]


# Update forward references for recursive-like schemas
PyItemOut.update_forward_refs()
PyTagOut.update_forward_refs()


# %%%%%%%%%%%%%%%%%%%%%%%
# crud.py
async def crud_create_item(session: AsyncSession, item: PyItemIn) -> Item:
    # Automatically commits if no exceptions are raised
    item_dict = item.dict()
    tag_names = item_dict.pop("tag_names")
    db_item = Item(**item_dict)  # type: ignore
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item, ["tags"])  # Flush to get the id

    for tag_name in tag_names:
        query = select(Tag).where(Tag.name == tag_name)
        db_tag = (await session.execute(query)).scalar_one_or_none()
        # If tag does not exist, create it
        if db_tag is None:
            db_tag = Tag(name=tag_name)
            session.add(db_tag)

        db_item.tags.append(db_tag)

    await session.commit()
    return db_item


async def crud_get_item_or_none(session: AsyncSession, item_id: int) -> Item | None:
    query = select(Item).where(Item.id == item_id).options(orm.selectinload(Item.tags))
    async with session.begin():
        item = await session.execute(query)
    return item.scalar_one_or_none()


async def crud_get_items(session: AsyncSession, limit: int = 100, offset: int = 0) -> Sequence[Item]:
    query = select(Item).options(orm.selectinload(Item.tags)).limit(limit).offset(offset)
    async with session.begin():
        items = await session.execute(query)
    return items.scalars().all()


async def crud_create_tag(session: AsyncSession, tag: PyTagIn) -> Tag:
    async with session.begin():
        tag_db = Tag(**tag.dict())
        session.add(tag_db)
    return tag_db


async def crud_get_tags(session: AsyncSession, limit: int = 100, offset: int = 0) -> Sequence[Tag]:
    query = select(Tag).limit(limit).offset(offset)
    async with session.begin():
        tags = await session.execute(query)
    return tags.scalars().all()


async def crud_get_tag_or_none(session: AsyncSession, tag_id: int) -> Tag | None:
    query = select(Tag).where(Tag.id == tag_id).options(orm.selectinload(Tag.items))
    async with session.begin():
        tag_db = await session.execute(query)
    return tag_db.scalar_one_or_none()

# %%%%%%%%%%%%%%%%%%%%%%%
# dependencies.py


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SESSION_FACTORY() as session:
        try:
            yield session
        except IntegrityError:
            await session.rollback()


# %%%%%%%%%%%%%%%%%%%%%%%
# main.py

APP = FastAPI()


@APP.get("/")
async def root():
    return {"message": "Hello World"}


@APP.get("/items/", response_model=list[PyItemOut], tags=["items"])
async def get_items(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)):
    return await crud_get_items(session, limit, offset)


@APP.post("/items/", response_model=PyItemOut, tags=["items"])
async def create_item(item: PyItemIn, session: AsyncSession = Depends(get_session)):
    return await crud_create_item(session, item)


@APP.get("/items/{item_id}", response_model=PyItemOut, tags=["items"])
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await crud_get_item_or_none(session, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    return item


@APP.post("/tags/", response_model=PyTagOut, tags=["tags"])
async def create_tag(tag: PyTagIn, session: AsyncSession = Depends(get_session)):
    return await crud_create_tag(session, tag)


@APP.get("/tags/", response_model=list[PyTagOutMinimal], tags=["tags"])
async def get_tags(session: AsyncSession = Depends(get_session)):
    return await crud_get_tags(session)


@APP.get("/tags/{tag_id}", response_model=PyTagOut, tags=["tags"])
async def get_tag(tag_id: int, session: AsyncSession = Depends(get_session)):
    tag = await crud_get_tag_or_none(session, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")
    return tag


@APP.on_event("startup")
# Create tables on startup; this is not a good idea and instead you should use alembic migrations
async def create_tables() -> None:
    async with ENGINE.begin() as conn:
        await conn.run_sync(METADATA.create_all)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(APP)