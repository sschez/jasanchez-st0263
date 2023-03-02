from flask import Flask, jsonify, request
import grpc
import os

import list_files_pb2, list_files_pb2_grpc

app = Flask(__name__)

# Se configura la dirección y puerto del servidor gRPC
grpc_server_address = os.environ.get("GRPC_SERVER_ADDRESS", "localhost:50051")

# Se crea un canal de comunicación con el servidor gRPC
grpc_channel = grpc.insecure_channel(grpc_server_address)

# Cliente para el servicio de ListFiles
list_files_client = list_files_pb2_grpc.ListFilesStub(grpc_channel)

@app.route("/files")
def list_files():
    response = list_files_client.GetFilesList(list_files_pb2.ListFilesRequest())
    return jsonify({"files": [file.filename for file in response.files]})

# INCOMPLETO 
@app.route('/search_files')
def search_files():
    query = request.args.get('query')
    files_list = serv2_stub.SearchFiles(search_files_pb2.SearchFilesRequest(query=query))
    response = {}
    response['files'] = [f.filename for f in files_list.files]
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
