import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def calculate(body):
    values = body.split()
    if(values[2].decode("utf-8") is "+"):
        return(float(values[0]) + float(values[1]))
    elif(values[2].decode("utf-8") is "-"):
        return(float(values[0]) - float(values[1]))
    elif(values[2].decode("utf-8") is "/"):
        return(float(values[0]) / float(values[1]))
    elif(values[2].decode("utf-8") is "*"):
        return(float(values[0]) * float(values[1]))
    return 0;

def on_request(ch, method, props, body):
    print(" [x]  %r" % body)
    response = calculate(body)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
