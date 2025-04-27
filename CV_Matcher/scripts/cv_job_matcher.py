import asyncio
from scripts.repo.redis_repo import main

if __name__ == '__main__':
    print("Running Redis listener...")
    asyncio.run(main())