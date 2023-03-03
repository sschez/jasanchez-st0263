from flask import Flask, request, jsonify
import pika
import uuid
import os

app = Flask(__name__)

# Configuración de RabbitMQ

class RpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.correlation_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

# Configuración de cola de mensajes
class MomClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='file_search')

    def search_file(self, filename):
        self.channel.basic_publish(
            exchange='',
            routing_key='file_search',
            body=filename)

# Rutas de API
@app.route('/list_files')
def list_files():
    files = os.listdir()
    return jsonify(files)

@app.route('/search_file')
def search_file():
    filename = request.args.get('filename')
    if not filename:
        return 'Falta el parámetro "filename"', 400
    mom_client = MomClient()
    mom_client.search_file(filename)
    rpc_client = RpcClient()
    result = rpc_client.call(0)
    if result == 1:
        return 'El archivo "{}" se encontró.'.format(filename)
    else:
        return 'El archivo "{}" no se encontró.'.format(filename)

if __name__ == '__main__':
    app.run(debug=True)
