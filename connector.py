import asyncio

from simulator import Simulator


async def main():
    file = open('data.txt', 'w', newline='')

    evl = asyncio.get_event_loop()
    evl.create_task(Simulator().simulate(file))
    evl.run_forever()

if __name__ == "__main__":
    asyncio.run(main())
