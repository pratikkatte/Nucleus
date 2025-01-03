import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from pathlib import Path


app = FastAPI()

server_instance = None

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

react_build_dir = Path(__file__).parent / "../visualization/dist"

uploads_dir = os.curdir

app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

app.mount("/assets", StaticFiles(directory=react_build_dir / "assets"), name="assets")

# Serve the index.html for the root endpoint
@app.get("/")
async def serve_react_app():
    index_file = react_build_dir / "index.html"
    return FileResponse(index_file)


@app.get("/status")
async def status():
    return {"status": "Running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        server_instance = websocket.app.state.server_instance
        while True:
            if server_instance and not server_instance.data_queue.empty():
                data_to_send = server_instance.data_queue.get()
                try:
                    await asyncio.sleep(1)
                    await websocket.send_json(data_to_send)
                except WebSocketDisconnect:
                    print("WebSocket connection closed while sending data.")
                    # break
                except Exception as e:
                    print(f"Error while sending data: {e}")
                    break
            else:
                # Check for a condition to break the loop to avoid infinite wait
                if not server_instance.running:
                    print("Exiting loop due to condition.")
                    break
                await asyncio.sleep(0.1)  # Allow the loop to wait briefly
                
    except WebSocketDisconnect:
        print("WebSocket connection closed by the client.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        print("WebSocket endpoint cleanup.")
