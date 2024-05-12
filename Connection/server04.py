from flask import Flask, request
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
