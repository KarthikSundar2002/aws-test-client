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
    # my_config = Config(
    #     region_name='ap-south-1',
    #     signature_version='s3v4',
    #     retries={
    #         'max_attempts': 10,
    #         'mode': 'standard'
    #     }
    # )

    # # def create_bucket(s3_resource):
    # #     bucket_name = f'test-bucket-{uuid.uuid4()}'
    # #     bucket = s3_resource.Bucket(bucket_name)
    # #     try:
    # #         bucket.create(
    # #             CreateBucketConfiguration={
    # #                 'LocationConstraint': s3_resource.meta.client.meta.region_name
    # #             }
    # #         )
    # #         print(f"{bucket_name} created")
    # #         return bucket
    # #     except ClientError as e:
    # #         print(f"Tried and failed to create demo bucket {bucket_name}.")
    # #         print(
    # #             f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}")
    # #         print(f"\nCan't continue the demo without a bucket!")
    # #         return

    # def usage_demo():
    #     parser = argparse.ArgumentParser(description="AWS client POC")
    #     parser.add_argument('bucket', help="The name of the bucket.")
    #     parser.add_argument(
    #         'key', help="For a GET operation, the key of the object in Amazon S3. For a PUT operation, the name of a file to upload.")
    #     parser.add_argument(
    #         'action', choices=('get', 'put'), help="The action to perform.")
    #     args = parser.parse_args()

    #     s3_client = boto3.client('s3', config=my_config)
    #     client_action = 'get_object' if args.action == 'get' else 'put_object'
    #     url = generate_presigned_url(
    #         s3_client, client_action, {'Bucket': args.bucket, 'Key': args.key}, 1000)

    #     print("Using the Requests package to send a request to the URL.")
    #     response = None
    #     if args.action == 'get':
    #         response = requests.get(url)
    #     elif args.action == 'put':
    #         print("Putting data to the URL.")
    #         try:
    #             with open(args.key, 'r') as object_file:
    #                 object_text = object_file.read()
    #             response = requests.put(url, data=object_text)
    #         except FileNotFoundError:
    #             print("the key must be the name of a file that exists on your computer")

    #     if response is not None:
    #         print("Got response:")
    #         print(response.text)

    # if __name__ == '__main__':
    #     usage_demo()
