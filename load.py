#!/usr/bin/env python3

import os
import sys
import aiohttp
import asyncio
from pprint import pprint


async def fetch(session: aiohttp.ClientSession, url: str, num: int):
    async with session.post(url, json={"number": num}) as response:
        return await response.json()


async def send(url: str, min_: int, max_: int):
    async with aiohttp.ClientSession() as session:
        req = []
        for n in range(min_, max_ + 1):
            req.append(fetch(session, url, n))

        res = await asyncio.gather(*req, return_exceptions=True)

        pprint(res)


def main():
    loop = asyncio.get_event_loop()

    min_ = os.getenv("MIN")
    if not min_:
        print("MIN env required")
        return
    try:
        min_ = int(min_)
    except ValueError:
        print("MIN should be int")
        return

    max_ = os.getenv("MAX")
    if not max_:
        print("MAX env required")
        return
    try:
        max_ = int(max_)
    except ValueError:
        print("MAX should be int")

    url = os.getenv("URL")
    if not url:
        print("URL env required")
        return

    loop.run_until_complete(send(url, min_, max_))


if __name__ == "__main__":
    main()
