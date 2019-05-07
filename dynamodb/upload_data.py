import boto3
import json

json_file = 'data.json'
table_name = 'deepheels'
aws_region = 'us-east-1'

table = boto3.resource('dynamodb', region_name=aws_region).Table(table_name)

with open(json_file) as f:
	data = json.load(f)

with table.batch_writer() as batch:
	for item in data:
		batch.put_item(Item = item)
