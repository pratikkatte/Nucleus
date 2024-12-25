from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

# Start a shell session
@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.json
    print(data)
    command = data.get('command')
    if not command:
        return jsonify({"error": "No command provided"}), 400

    try:
        # Start a new bash session with the current working directory
        result = subprocess.run(
            f"bash -c '{command}'",  # Run command within a bash shell
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        response = {
            "output": str(result.stdout),
            "error": result.stderr,
            "return_code": result.returncode
        }
        print(result, response)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
