# DeepHeels

Discover fab heels and cool kicks by selecting styles you like. 

[ML Jupyter Notebook](https://github.com/aws-samples/aws-sagemaker-pytorch-shop-by-style) – [Shoe dataset](http://vision.cs.utexas.edu/projects/finegrained/utzap50k/) – [Website demo](http://deepheels.s3-website-us-east-1.amazonaws.com/)

## Getting Started

These instructions will get you a copy of the project up and running on AWS.

### Prerequisites

What you'll need to get started:
* [AWS Account](https://aws.amazon.com/)
* [Boto 3](https://pypi.org/project/boto3/), installed and configured
* (Optional) Use [our dataset](https://github.com/tobjensen/deepheels/blob/master/dynamodb/data.json) from this repo or train your own with dataset with this [ML Jupyter Notebook](https://github.com/aws-samples/aws-sagemaker-pytorch-shop-by-style)

### Installing

[Create a new table](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table) on DynamoDB with 'id' as the primary key

```
import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.create_table(
    TableName='deepheels',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)
```

Populate the DynamoDB table with the [data](https://github.com/tobjensen/deepheels/blob/master/dynamodb/data.json)
```
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
```

Populate the DynamoDB table with the [data](https://github.com/tobjensen/deepheels/blob/master/dynamodb/data.json)
```
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
```

Create an IAM role for the Lambda functions, allowing them to read from DynamoDB and write logs
```
import boto3
import json

iam = boto3.client('iam')

policy = json.dumps({
	'Statement': [
		{
		'Effect': 'Allow',
		'Principal': {
			'Service': 'lambda.amazonaws.com'
		},
		'Action': 'sts:AssumeRole'
		}
	]
})

iam.create_role(
	RoleName = 'lambda-dynamo',
	AssumeRolePolicyDocument = policy)

iam.attach_role_policy(
    RoleName='lambda-dynamo', 
    PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole')

iam.attach_role_policy(
    RoleName='lambda-dynamo', 
    PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess')
```

Pack up the functions and their data in .zip files
```
zip grid.zip grid.py shoes.csv
zip like.zip like.py
```

Deploy the two Lambda functions to AWS
```
import boto3

lambda_client = boto3.client('lambda')
role = boto3.resource('iam').Role('lambda-dynamo')

for function in ('grid', 'like'):
	with open(f'{function}.zip', 'rb') as f:
		code = f.read()

	lambda_client.create_function(
		FunctionName =f'{function}',
		Runtime ='python3.7',
		Role = role.arn,
		Handler = f'{function}.lambda_handler',
		Code = {'ZipFile': code})
```

Set up an API endpoint with API Gateway.

Below are the steps to set up the API endpoint through the console.
You can leave all the defaults as they are.

You'll do this twice, one for each Lambda functions.

* Navigate to API Gateway and press 'Create API'
* Give your API a name (first 'grid', then 'like')
* Press 'Actions' and then 'Create Ressource'
* Give the ressource a name (first 'grid', then 'like') and press 'Create Resource'
* Press 'Actions', then 'Create Method', choose 'POST' and press ✅
* Type in the name of the Lambda function (first 'grid', then 'like') and press 'Save'
* Press 'Actions', then 'Enable CORS' and press 'Enable CORS and replace existing CORS headers'
* Press 'Actions' and then 'Deploy API'
* Choose `[New Stage]` as Deployment stage and give it a name (ex: `api`)
* Press the ▶ next to `1` to unfold the menu and press 'POST' to see Invoke URL
* Take note of the URL for the API endpoints (ex: `https://xxxxxx.execute-api.us-east-1.amazonaws.com/api`)

Insert the API endpoints you just create in [deep.js](https://github.com/tobjensen/deepheels/blob/master/website/deep.js)

Upload the website files to S3. 
Make sure you've created a bucket with [public read access](https://docs.aws.amazon.com/AmazonS3/latest/dev/example-bucket-policies.html#example-bucket-policies-use-case-2) and enabled [website hosting](https://docs.aws.amazon.com/AmazonS3/latest/dev/EnableWebsiteHosting.html).

```
aws s3 sync website s3://YOUR_BUCKET/
```

You should be all set. 
Check out the [website demo](http://deepheels.s3-website-us-east-1.amazonaws.com/) for a live example.


## Built With

* [Python](http://www.dropwizard.io/1.0.2/docs/) - Application & Deployment
* [Lambda](http://www.dropwizard.io/1.0.2/docs/) - Serverless computing
* [DynamoDB](http://www.dropwizard.io/1.0.2/docs/) - NoSQL database service
* [API Gateway](http://www.dropwizard.io/1.0.2/docs/) - Creating APIs
* [S3](http://www.dropwizard.io/1.0.2/docs/) - Hosting website and images
* [jQuery](http://www.dropwizard.io/1.0.2/docs/) - Inserting images on webpage


## Authors

* **Tobias Jensen** - [GitHub](https://github.com/tobjensen)

## Acknowledgments

* Dylan Tong (AWS) [ML Jupyter Notebook](https://github.com/aws-samples/aws-sagemaker-pytorch-shop-by-style)
* A. Yu and K. Grauman (University of Texas) [UT Zappos50K shoe dataset](http://vision.cs.utexas.edu/projects/finegrained/utzap50k/)
