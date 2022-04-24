import asyncio
import uvloop
import logging

logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] | %(asctime)s >> %(message)s",  datefmt='[%m/%d/%Y | %I:%M:%S %p %Z]'
    )

async def main():
    while True:
        await asyncio.sleep(3)
        logging.info("Hello World")
    
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.new_event_loop()
asyncio.ensure_future(main(), loop=loop)
loop.run_forever()