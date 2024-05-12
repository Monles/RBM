from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    
    # Process and save data to a file
    save_data(data)
    
    return 'Data received successfully!', 200

def save_data(data):
    # Write data to a JSON file
    with open('received_data.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
