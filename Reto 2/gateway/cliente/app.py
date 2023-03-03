from flask import Flask, jsonify, request
import pika
import uuid
import json

app = Flask(__name__)

@app.route('/search_file', methods=['POST'])
def search_file():
    # Se establece una conexión con RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('guest', 'guest')))
    channel = connection.channel()

    # Se declara la cola en la que se enviará el mensaje de búsqueda
    channel.queue_declare(queue='file_search')

    # Se envía el mensaje al productor
    search_param = request.get_json()['search_param']
    correlation_id = str(uuid.uuid4())
    channel.basic_publish(
        exchange='search_files',
        routing_key='file_search',
        body=search_param,
        properties=pika.BasicProperties(
            reply_to='file_search_response',
            correlation_id=correlation_id
        )
    )

    # Se espera la respuesta del consumidor
    def on_response(ch, method, props, body):
        if props.correlation_id == correlation_id:
            response = json.loads(body.decode('utf-8'))
            print(response)
            connection.close()

    channel.basic_consume(
        queue='file_search_response',
        on_message_callback=on_response,
        auto_ack=True
    )

    channel.start_consuming()

    return jsonify({'message': 'Search request sent successfully!'})

if __name__ == '__main__':
    app.run(debug=True)

