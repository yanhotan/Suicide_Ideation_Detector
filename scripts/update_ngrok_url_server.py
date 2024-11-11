from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/update-ngrok-url', methods=['POST'])
def update_ngrok_url():
    data = request.json
    ngrok_url = data.get('ngrok_url')

    if ngrok_url:
        files = [
            'src/environments/environment.ts',
            'src/environments/environment.prod.ts'
        ]
        for file_path in files:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                new_content = re.sub(r"apiUrl: 'https?://.*?'", f"apiUrl: '{ngrok_url}'", content)
                with open(file_path, 'w') as file:
                    file.write(new_content)
                print(f"Updated {file_path} with new URL: {ngrok_url}")
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        return jsonify({"message": "Files updated successfully"}), 200
    else:
        return jsonify({"error": "No URL provided"}), 400

if __name__ == '__main__':
    app.run(port=4000, debug=True)
