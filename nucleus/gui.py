
import os
from flask import Flask, cli, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
import logging
import time
from threading import Thread
from pkg_resources import resource_filename

# Disable flask logging
# log = logging.getLogger('werkzeug')

# log.setLevel(logging.ERROR)
# log.disabled = True

# cli.show_server_banner = lambda *_: Nonce

frontend_path = resource_filename(__name__, 'gui/dist/')

data = {"assembly": {
  "name": 'NC_045512',
  "aliases": ['hg38'],
  "sequence": {
    "type": 'ReferenceSequenceTrack',
    "trackId": 'GRCh38-ReferenceSequenceTrack',
    "adapter": {
      "type": 'IndexedFastaAdapter',
      "fastaLocation": {
        "uri": 'http://127.0.0.1:5000/uploads/data/reference/NC_045512v2.fa',
      },
      "faiLocation": {
        "uri": 'http://127.0.0.1:5000/uploads/data/reference/NC_045512v2.fa.fai',
      },
    },
  }
},
"track": [{
        "type": 'AlignmentsTrack',
        "trackId": "genes", 
        "name": 'spike-in_bams_file_0.bam',
        "assemblyNames": ['NC_045512'],
        "category": ['Genes'],
        "adapter": {
          "type": 'BamAdapter',
          "bamLocation": {
            "uri": 'http://127.0.0.1:5000/uploads/data/bamfiles/customised_my_vcf_NODE-1.bam',
          },
          "index": {
            "location": {
              "uri": 'http://127.0.0.1:5000/uploads/data/bamfiles/customised_my_vcf_NODE-1.bam.bai',
            },
          },
        }
    }]
}
app = Flask(__name__,  static_folder=frontend_path)

UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__))

print("UPLOAD_FOLDER", UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

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

# Test GET endpoint
@app.route('/', methods=['GET'])
def status():
    print("Status endpoint accessed")
    return "Success 200!"


@socketio.on("data")
def send_data():
    global data
    while True:
        time.sleep(5)  # Wait for 5 seconds before sending an update
        # data = {'message': 'Hello from Flask!'}
        socketio.emit('data', {'message': data})

# Start the background thread that sends data updates
def start_background_task():
    thread = Thread(target=send_data)
    thread.daemon = True
    thread.start()


def run_flask_app(file_input):

    # from werkzeug.serving import make_server
    # http_server = make_server('127.0.0.1', 5000, app)
    print(file_input)
    if not file_input:
        print("Provide the file that you want to show!")
        return
    else:
        # http_server.serve_forever()
        socketio.run(app, host='127.0.0.1', port=5000, debug=True)


if __name__ == '__main__':
    # app.run(debug=True)
    start_background_task()
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)

