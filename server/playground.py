from completion import stream_completion
import asyncio

async def print_completion():
    async for x in stream_completion("Write a poem on America in 50 words or less"):
        print(x)

if __name__ == "__main__":
    asyncio.run(print_completion())