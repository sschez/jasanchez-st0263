import pika
import os

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials("guest", "guest")))
channel = connection.channel()

channel.queue_declare(queue='archivo_rpc')

def on_request(ch, method, props, body):
    filename = body.decode()
    response = buscar_archivo(filename)
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def buscar_archivo(filename):
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files:
            return f"El archivo {filename} se encuentra en el microservicio." #os.path.join(root, filename)
    return f"No se ha encontrado el archivo {filename} en el microservicio."
    #if os.path.isfile(filename):
     #   return f"El archivo {filename} se encuentra en el microservicio."
    #else:
     #   return f"No se ha encontrado el archivo {filename} en el microservicio."
    

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='archivo_rpc', on_message_callback=on_request)

print("Esperando por solicitudes...")
channel.start_consuming()

