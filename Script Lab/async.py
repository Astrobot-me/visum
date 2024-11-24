import asyncio 


async def fetch_data(id,delay):
    print(f"Fectching Data id: {id}")
    await asyncio.sleep(delay)
    print(f"Data fetched for id: {id} ")
    return {'id':id}


async def main():
    task1 = asyncio.create_task(fetch_data(1,3))
    task2 = asyncio.create_task(fetch_data(2,2))
    task3 = asyncio.create_task(fetch_data(3,4))

    result1 = await task1 
    result2 = await task2 
    result3 = await task3

    print(result1,result2,result3)


asyncio.run(main())