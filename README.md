# aws-test-client

A test AWS S3 client written using python, boto3 and AWS SDK. 
Before you run the program make sure you change the access key id and secret access key in the client and resource. 
After changing those, you can run the program. As of now, we can create buckets and we can access the existing buckets. Basically as of now, when we access a bucket, it searches test.txt. Using this file, it generates a presigned URL, which allows us to see the contents of text.txt
