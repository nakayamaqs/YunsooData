import boto
from boto.s3.key import Key
from boto.s3.connection import Location
# Instantiate a new client for Amazon Simple Storage Service (S3). With no
# parameters or configuration, the AWS SDK for Python (Boto) will look for
# access keys in these environment variables:
#
#    AWS_ACCESS_KEY_ID='...'
#    AWS_SECRET_ACCESS_KEY='...'
#
# For more information about this interface to Amazon S3, see:
# http://boto.readthedocs.org/en/latest/s3_tut.html

conn = boto.s3.connect_to_region('cn-north-1')
# bucketname = 'yunsudev-1'
# b = conn.create_bucket(bucketname, location=Location.CNNorth1)

ys_bucket = conn.get_bucket("yunsudev")

def save_content(fullkey, content):
    k = Key(ys_bucket)
    k.key = fullkey
    # 'python_sample_key.txt'

    print("Uploading some data to " + str(ys_bucket) + " with key: " + k.key)
    headers = {'Content-Type': 'application/json'}
    k.set_contents_from_string(content, headers=headers)


# save_content('report/organization/2k0r1l55i2rs5544wz5', 'hello,data!')
