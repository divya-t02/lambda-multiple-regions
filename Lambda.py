import json
import boto3
import os


def lambda_handler(event, context):
ssmKey = event['detail']['name']

client = boto3.client('ssm')
response = client.get_parameter(Name=f"/{ssmKey}")
ssmValue = response['Parameter']['Value']

amiRegion = 'us-west-2'
regions = os.environ['region'].split(',')
for region in regions:
client = boto3.client('ec2', region_name=region)
response = client.copy_image(
Name="Base Image",
Description=f"Copy of {ssmValue}",
SourceImageId=ssmValue,
SourceRegion=amiRegion
)

return {
'statusCode': 200,
'body': json.dumps('AMI Copied successfully')
}
