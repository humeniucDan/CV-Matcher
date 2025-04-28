import asyncio
from scripts.repo.redis_repo import main
from db_configure import create_tables

if __name__ == '__main__':
    asyncio.run(main())