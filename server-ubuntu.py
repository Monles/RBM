from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    if data:
        # Extract timestamp from data
        timestamp = data.get('timestamp', None)
        if timestamp:
            # Convert timestamp to filename format
            filename = f"{timestamp}.data"
            # Save data to file
            with open(filename, 'w') as file:
                json.dump(data, file)
            print(f"Data received and saved to file: {filename}")
            return "Data received and saved successfully!", 200
        else:
            return "Timestamp not found in the data", 400
    else:
        return "No data received", 400

@app.route('/receive_screenshot', methods=['POST'])
def receive_screenshot():
    if 'file' not in request.files:
        return "No file part in the request", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file", 400
    
    if file:
        filename = file.filename
        save_path = os.path.join(os.getcwd(), filename)
        file.save(save_path)
        print(f"Screenshot received and saved to file: {save_path}")
        return "Screenshot received and saved successfully!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
