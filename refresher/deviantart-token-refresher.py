import asyncio
import os
import aiohttp
import orjson
from dotenv import load_dotenv
from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.ext.asyncio import create_async_engine
import logging

load_dotenv()

Client_ID = os.getenv("DeviantArt_Client_ID")
Client_Secret = os.getenv("DeviantArt_Client_Secret")
Password = os.getenv("Postgres_Rin_Password")
Server_IP = os.getenv("Postgres_Server_IP")
Username = os.getenv("Postgres_Username")

logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] | %(asctime)s >> %(message)s",  datefmt='[%m/%d/%Y] [%I:%M:%S %p %z]'
    )

class tokenRefresherUtils:
    def __init__(self):
        self.self = self

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
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/rin_deviantart_tokens_v3"
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

async def main():
    while True:
        await asyncio.sleep(3330)
        tokens = tokenRefresherUtils()
        values = await tokens.get()
        logging.info(f"Tokens from DB: {values}")
        Refresh_Token_Select = values[1]
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "client_id": f"{Client_ID}",
                "client_secret": f"{Client_Secret}",
                "grant_type": "refresh_token",
                "refresh_token": f"{Refresh_Token_Select}",
            }
            async with session.get(
                "https://www.deviantart.com/oauth2/token", params=params
            ) as r:
                data = await r.json()
                Access_token = data["access_token"]
                Refresh_token = data["refresh_token"]
                logging.info(f"Values from API Request - {Access_token}, {Refresh_token}")
                await tokens.update_values(Access_token, Refresh_token)
        
loop = asyncio.new_event_loop()
asyncio.ensure_future(main(), loop=loop)
loop.run_forever()