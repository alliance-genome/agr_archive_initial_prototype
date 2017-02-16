
import boto3
s3 = boto3.client('s3')
#mod-datadumps
#bucket = s3.Bucket('mod-datadumps')
#for item in bucket.objects.all():
#	print(item)

s3.download_file('mod-datadumps', 'MGI_0.3.0_1.tar.gz', 'tmp/MGI_0.3.0_1.tar.gz')

