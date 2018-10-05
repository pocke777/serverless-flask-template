import json
import os
import uuid
import boto3
from io import StringIO
from flask import Flask, request, jsonify

import subprocess as sp

from handlers import users

FFMPEG_PATH = './bin/ffmpeg'

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

app.register_blueprint(users.app)

s3 = boto3.resource('s3')
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

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

@app.route("/audio")
def audio():
    id = uuid.uuid1().hex
    res = sp.call([
        FFMPEG_PATH,
        '-i', 'binary/party.mp3',
        '-i', 'binary/yattaze!2.mp3',
        '-filter_complex', '[1]adelay=2000|2000[b]; [0][b]amix=inputs=2',
        '-y', '/tmp/out.mp3'
    ])

    print(res)
    s3.Bucket(S3_BUCKET_NAME).upload_file('/tmp/out.mp3', 'audio/%s/%s%s'%(id, uuid.uuid1(), '.mp3'))

    return "ok"

