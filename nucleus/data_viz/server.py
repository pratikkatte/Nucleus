import uvicorn
from threading import Thread
import asyncio
from fastapi import FastAPI
import time
from queue import Queue



class FastAPIServer:
    def __init__(self, app: FastAPI, host: str = "127.0.0.1", port: int = 8000):
        self.app = app
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
        self.loop = None
        self.data_queue = Queue()
        self.running = False

    def start(self):
        """Starts the FastAPI server in a separate thread."""

        self.running = True

        if self.thread and self.thread.is_alive():
            # print("FastAPI server is already running.")
            return False

        def run_server():
            """Run the server inside an event loop."""
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            config = uvicorn.Config(self.app, host=self.host, port=self.port, log_level="error")
            self.server = uvicorn.Server(config)
            self.loop.run_until_complete(self.server.serve())

        self.thread = Thread(target=run_server, daemon=True)
        self.thread.start()
        # print(f"FastAPI server started on http://{self.host}:{self.port}")

    def stop(self):
        """Stops the FastAPI server."""
        self.running = False
        if self.server and self.loop:

            # print("Stopping FastAPI server...") # needs to be added to log file
            self.loop.call_soon_threadsafe(lambda: setattr(self.server, "should_exit", True))
            self.thread.join()  # Wait for the thread to finish

            if self.thread.is_alive():
                # print("thread is still alive")
                pass

    def send_data(self, data):
        """Send data to the queue."""
        self.data_queue.put(data)


