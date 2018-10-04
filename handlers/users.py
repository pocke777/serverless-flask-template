import os
import uuid

import boto3
from botocore.exceptions import ClientError
from flask import Blueprint, request, jsonify

app = Blueprint("users", __name__)

s3 = boto3.resource('s3')
USERS_TABLE = os.environ['USERS_TABLE']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

IS_OFFLINE = os.environ.get('IS_OFFLINE')
if IS_OFFLINE:
    dynamodb = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000',
    )
else:
    dynamodb = boto3.client('dynamodb')



@app.route("/users")
def index():
    return "Users Index"

@app.route("/users/<id>")
def show(id):
    return "Users Show"

@app.route("/users", methods=["POST"])
def create():

    id = uuid.uuid1().hex
    file = request.files['image']
    _n, ext = os.path.splitext(file.filename)

    try:
        obj = s3.Object(
            S3_BUCKET_NAME,
            'images/%s/%s%s'%(id, uuid.uuid1(), ext)
        )

        res = obj.put(
            Body=file,
            ACL="public-read",
            ContentType=file.content_type
        )
    except:
        return jsonify({ 'errors': 's3 connection error' })

    if res['ResponseMetadata']['HTTPStatusCode'] != 200:
        return jsonify({ 'message': 'ng' })

    res = dynamodb.put_item(
        TableName=USERS_TABLE,
        Item={
            'image_path': {'S': obj.key },
            'userId': {'S': id },
        }
    )

    return jsonify({ 'path': obj.key })
