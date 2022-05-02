import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.ext.asyncio import create_async_engine
import logging
import uvloop

load_dotenv()

Client_ID = os.getenv("DeviantArt_Client_ID")
Client_Secret = os.getenv("DeviantArt_Client_Secret")
Password = os.getenv("Postgres_Rin_Password")
Server_IP = os.getenv("Postgres_Server_IP")
Username = os.getenv("Postgres_Username")

Access_Token = os.getenv("DeviantArt_Access_Token")
Refresh_Token = os.getenv("DeviantArt_Refresh_Token")

logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] | %(asctime)s >> %(message)s",  datefmt='[%m/%d/%Y] - [%I:%M:%S %p %Z]'
    )

class tokenRefresherUtilsMain:
    def __init__(self):
        self.self = self
    
    async def initTable(self):
        meta4 = MetaData()
        engine4 = create_async_engine(
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/rin_deviantart_tokens_v3", echo=True
        )
        tokens = Table(
            "DA_Tokens",
            meta4,
            Column("Access_Tokens", String),
            Column("Refresh_Tokens", String),
        )
        async with engine4.begin() as conn4:
            await conn4.run_sync(meta4.create_all)
            
    async def get(self):
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/rin_deviantart_tokens_v3"
        )
        tokens = Table(
            "DA_Tokens",
            meta,
            Column("Access_Tokens", String),
            Column("Refresh_Tokens", String),
        )
        async with engine.connect() as conn:
            s = tokens.select()
            result_select = await conn.stream(s)
            async for row in result_select:
                return row
            
    async def update_values(self, Access_Token, Refresh_Token):
        meta = MetaData()
        engine2 = create_async_engine(
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/rin_deviantart_tokens_v3", echo=True
        )
        tokens = Table(
            "DA_Tokens",
            meta,
            Column("Access_Tokens", String),
            Column("Refresh_Tokens", String),
        )
        async with engine2.begin() as conn2:
            update = tokens.update().values(
                Access_Tokens=f"{Access_Token}", Refresh_Tokens=f"{Refresh_Token}"
            )
            await conn2.execute(update)
            
    async def insert_values(self, Access_Token, Refresh_Token):
        meta = MetaData()
        engine2 = create_async_engine(
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/rin_deviantart_tokens_v3", echo=True
        )
        tokens = Table(
            "DA_Tokens",
            meta,
            Column("Access_Tokens", String),
            Column("Refresh_Tokens", String),
        )
        async with engine2.begin() as conn2:
            update = tokens.insert().values(
                Access_Tokens=f"{Access_Token}", Refresh_Tokens=f"{Refresh_Token}"
            )
            await conn2.execute(update)

async def main():
    token = tokenRefresherUtilsMain()
    # await token.update_values(Access_Token, Refresh_Token)
    await token.insert_values(Access_Token, Refresh_Token)
    # print(await token.get())

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
