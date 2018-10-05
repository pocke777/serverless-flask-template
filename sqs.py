import os
import uuid
import boto3

s3 = boto3.resource('s3')
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

def handler(event, context):
    print(event)
    for record in event['Records']:
        print(record['body'])

        id = uuid.uuid1().hex
        try:
            s3.Bucket(S3_BUCKET_NAME).upload_file('binary/pickrusu.jpg', 'images/%s/%s%s'%(id, uuid.uuid1(), '.jpg'))
        except:
            return jsonify({ 'errors': 's3 connection error' })
    return "ok"
