#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   async_test.py
@Time    :   2020/09/06 21:15:22
@Author  :   Liu Yimin
@Version :   1.0
@Contact :   chentuliu@126.com
@License :   (C)Copyright 2020-2021, LiuYimin-NLPR-CASIA
@Desc    :   None
'''

import time
import asyncio


async def hi(msg, sec):
    
    print(f"enter hi(), {msg} @ {time.strftime('%H:%M:%S')}")
    await asyncio.sleep(sec)
    print(f"{msg} @{time.strftime('%H:%M:%S')}")
    return sec


async def main():
    print(f"main() begin at {time.strftime('%H:%M:%S')}")
    tasks = []
    for i in range(1, 5):
        t = asyncio.create_task(hi(i, i))
        tasks.append(t)

    # print('main asyncio sleeping')
    # await asyncio.sleep(2)
    for i in tasks:
        r = await t
        print('r:', r)
    print(f"main() end at {time.strftime('%H:%M:%S')}")

asyncio.run(main())
