from flask import Flask, request

app = Flask(__name__)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    # Process received data
    print("Received data from Windows client:", data)
    return 'Data received successfully', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=<port>)
