import json
import boto3
from io import StringIO
from flask import Flask, request, jsonify

from handlers import users

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

app.register_blueprint(users.app)


@app.route("/")
def hello():
  return "Hello World!"


@app.route("/sqs/send")
def sender():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='SampleQueue')
    response = queue.send_message(MessageBody='create')
    print(response)

    return jsonify(response)
