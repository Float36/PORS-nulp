import asyncio

from src.app.core.db.database import init_db


async def _run() -> None:
    await init_db()
    print("Database tables are initialized.")


if __name__ == "__main__":
    asyncio.run(_run())
