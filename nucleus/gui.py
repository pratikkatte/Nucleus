
import os
from flask import Flask, cli, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
import logging
import time
from threading import Thread
from pkg_resources import resource_filename
from multiprocessing import Queue

# Disable flask logging
log = logging.getLogger('werkzeug')

log.setLevel(logging.ERROR)
log.disabled = True

cli.show_server_banner = lambda *_: None

frontend_path = resource_filename(__name__, 'visualization/dist')

app = Flask(__name__, static_folder='visualization/dist')


UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__))

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
CORS(app)  # Allow CORS for all origins

socketio = SocketIO(app, cors_allowed_origins="*",  async_mode="threading")

@app.route('/uploads/<path:name>')
def download_file(name):
    """Endpoint to download files."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

# Serve static files (e.g., JS, CSS)
@app.route('/assets/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)

# Serve the React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


@socketio.on("data")
def send_data():
    """
    """
    while True:
        time.sleep(5)  # Wait for 5 seconds before sending an update
        if not data_queue.empty():
            data = data_queue.get()
            socketio.emit('data', {'config': data})

def run_flask_app(queue):
    """
    """
    global data_queue
    data_queue = queue

    Thread(target=send_data, daemon=True).start()
      
    socketio.run(app, port=5000, debug=False, allow_unsafe_werkzeug=True, log_output=False)

if __name__ == '__main__':
    # global data_queue
    data_queue = Queue()
    data_queue.put({"message": "hello"})
    
    Thread(target=send_data, daemon=True).start()
    socketio.run(app, port=5000, debug=True)

