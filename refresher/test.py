import uvloop
import logging
import asyncio

logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] | %(asctime)s >> %(message)s",  datefmt='[%m/%d/%Y] [%I:%M:%S %p %z]'
    )

async def main():
    while True:
        await asyncio.sleep(3)
        logging.info("Hello World!!!!!!!!")
    
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())