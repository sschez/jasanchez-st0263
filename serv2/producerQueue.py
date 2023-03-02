import pika
import os
import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='file_search')

def search_file(ch, method, props, body):
    file_name = body.decode('utf-8')
    print("Buscando archivo %s..." % file_name)
    
    # Buscar el archivo en cualquier parte del servidor
    for root, dirs, files in os.walk('/'):
        if file_name in files:
            print("Archivo %s encontrado en %s" % (file_name, root))
            response = "Archivo encontrado en %s" % root
            break
    else:
        print("Archivo %s no encontrado" % file_name)
        response = "Archivo no encontrado"

    corr_id = props.correlation_id
    channel.basic_publish(exchange='',
                          routing_key=props.reply_to,
                          properties=pika.BasicProperties(correlation_id=corr_id),
                          body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # Modificar el estado del callback para terminar la comunicación
    #callback.finished = True

#class Callback:
 #   def __init__(self):
  #      self.finished = False

#callback = Callback()

channel.basic_consume(queue='file_search', on_message_callback=search_file)

print("Esperando mensajes del consumidor...")
#while not callback.finished:
   # connection.process_data_events()
channel.start_consuming()

#connection.close()
