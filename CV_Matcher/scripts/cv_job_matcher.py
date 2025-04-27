import asyncio
from scripts.repo.redis_repo import main
from db_configure import create_tables

if __name__ == '__main__':
    print("\033[92m[INFO] Starting Redis listener...\033[0m")
    print("\033[92m[INFO] Running Database config...\033[0m")
    try:
        create_tables()
        print("\033[92m[INFO] Tables created successfully!\033[0m")
        asyncio.run(main())
    except:
        print("\033[91m[ERROR] Failed to create tables!\033[0m")
        print("\033[91m[ERROR] Closing Redis listener...\033[0m")