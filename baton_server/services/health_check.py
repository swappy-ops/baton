import asyncio
import httpx
import sys
import os

async def check_health():
    print("Checking Baton Health...")
    
    # Check Backend
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://localhost:8000/docs")
            if resp.status_code == 200:
                print("✅ Backend: ONLINE")
            else:
                print(f"❌ Backend: ERROR ({resp.status_code})")
    except Exception:
        print("❌ Backend: OFFLINE")

    # Check SQLite
    db_path = "baton_server/db/baton.db"
    if os.path.exists(db_path):
        print("✅ Database: CONNECTED")
    else:
        print("❌ Database: MISSING")

    # Check WebSocket (Basic port check)
    import socket
    s = socket.socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    try:
        s.connect(("localhost", 8000))
        print("✅ WebSocket Port: OPEN")
    except Exception:
        print("❌ WebSocket Port: CLOSED")
    finally:
        s.close()

if __name__ == "__main__":
    asyncio.run(check_health())
