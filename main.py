import argparse
import logging
import boto3
from botocore.exceptions import ClientError
import requests
import uuid
from botocore.config import Config

logger = logging.getLogger(__name__)


def generate_presigned_url(s3_client, client_method, method_params, expires_in):
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method,
            Params=method_params,
            ExpiresIn=expires_in)
        logger.info("%s", url)
    except ClientError:
        logger.exception(
            "%s", client_method)
        raise
    return url


client = boto3.client(
    's3',
    aws_access_key_id="AKIA6F2OXH3ZJS7Q63NW",
    aws_secret_access_key="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",
    region_name="ap-south-1",
    endpoint_url="https://s3.ap-south-1.amazonaws.com",
    config=Config(signature_version='s3v4')
)

resource = boto3.resource(
    's3',
    aws_access_key_id="AKIA6F2OXH3ZJS7Q63NW",
    aws_secret_access_key="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",
    region_name="ap-south-1",
    config=Config(signature_version='v4')
)

clientResponse = client.list_buckets()

print('Printing bucket names...')
for bucket in clientResponse['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')

UserNeed = input(
    'Do you want to access (type "a") or create(type "c") buckets?')

if UserNeed == "c":
    bucketName = input('Enter the bucket name(It should be unique name): ')
    try:
        response = client.create_bucket(
            Bucket=bucketName,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1'
            }
        )
        print(response)
    except ClientError as e:
        logging.error(e)
        print(e)
elif UserNeed == "a":
    bucketName = input('Enter the bucket name you want to access: ')
    try:
        response = client.list_objects(
            Bucket=bucketName,
        )
        url = generate_presigned_url(
            client, "get_object", {'Bucket': bucketName, 'Key': 'test.txt'}, 1000)
        print(response)
        print(url)

    except ClientError as e:
        logging.error(e)
        print(e)

