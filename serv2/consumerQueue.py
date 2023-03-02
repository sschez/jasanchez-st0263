import pika
import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue
corr_id = str(uuid.uuid4())

def on_response(ch, method, props, body):
    if corr_id == props.correlation_id:
        print("Respuesta del servidor: %r" % body.decode('utf-8'))

class Callback:
    def __init__(self):
        self.finished = False

callback = Callback()

def search_file(file_name):    
    channel.basic_publish(exchange='',
                          routing_key='file_search',
                          properties=pika.BasicProperties(reply_to=callback_queue, correlation_id=corr_id),
                          body=str(file_name))
    channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)
    print("Enviando petición de búsqueda del archivo %s" % file_name)
    while not callback.finished:
        connection.process_data_events()
    channel.stop_consuming()
    connection.close()  


def on_response(ch, method, props, body):
    if corr_id == props.correlation_id:
        print("Respuesta del servidor: %r" % body.decode('utf-8'))
        callback.finished = True

print("Nombre del archivo a buscar: ")
file=input()
search_file(file)

