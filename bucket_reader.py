import boto3
from botocore.client import Config

# Initialize a session using DigitalOcean Spaces.
session = boto3.session.Session()
client = session.client('s3',
                        region_name='sgp1',
                        endpoint_url='https://sgp1.digitaloceanspaces.com',
                        aws_access_key_id='T73DNHQ2DPI4PB35JCDT',
                        aws_secret_access_key='eSsUdEHEqwaS7ph6VBnn8qnwtVhBf09hCXL0GdWzfzc')

# Create a new Space.
# client.create_bucket(Bucket='songs-1')

# List all buckets on your account.
response = client.list_buckets()
spaces = [space['Name'] for space in response['Buckets']]
print("Spaces List: %s" % spaces)