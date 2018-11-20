import pika
import string

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

result = channel.queue_declare(queue='',exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    values = body.split()
    result = 0
    if(values[2].decode("utf-8") is "+"):
        result = int(values[0]) + int(values[1])
    elif(values[2].decode("utf-8") is "-"):
        result = int(values[0]) - int(values[1])
    elif(values[2].decode("utf-8") is "/"):
        result = int(values[0]) / int(values[1])
    elif(values[2].decode("utf-8") is "*"):
        result = int(values[0]) * int(values[1])
    print(" [x] %r" % result)

channel.basic_consume(on_message_callback=callback,
                      queue=queue_name)

channel.start_consuming()
