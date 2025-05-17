from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

app = FastAPI()

@app.post("/heroes/")
async def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    await session.commit()
    await session.refresh(hero)
    return hero


@app.get("/heroes/")
async def read_heroes(
    session: SessionDep,
) -> Sequence[Hero]:
    heroes = (await session.execute(select(Hero))).scalars().all()
    return heroes


@app.get("/heroes/{hero_id}")
async def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = (await session.execute(select(Hero).where(Hero.id == hero_id))).scalar()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.delete("/heroes/{hero_id}")
async def delete_hero(hero_id: int, session: SessionDep):
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    await session.delete(hero)
    await session.commit()
    return {"ok": True}
