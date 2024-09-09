import json, os, pathlib, tempfile, shutil
import boto3

AWS_REGION = 'eu-central-1'
BASE = pathlib.Path().resolve()
LAMBDA_SRC = os.path.join(BASE, 'src')
IAM_CLIENT = boto3.client('iam')
LAMBDA_CLIENT = boto3.client('lambda', region_name=AWS_REGION)

boto3.setup_default_session(profile_name='booklink')
ec2_client = boto3.client("lambda", region_name=AWS_REGION)
iam = boto3.client('iam')
lambda_client = boto3.client('lambda')

role_policy = {"Version":"2012-10-17","Statement":[{"Sid":"","Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}

def archive_lambda(lambda_code):
    with tempfile.TemporaryDirectory() as td:
        lambda_archive_path = shutil.make_archive(td,'zip',root_dir=lambda_code)
    return lambda_archive_path

def create_role():
    response = iam.create_role(
        RoleName='LambdaBasicExecution',
        AssumeRolePolicyDocument=json.dumps(role_policy),
    )
    print(response)
    return response

def create_function(zip_file,function_name):
    with open(zip_file, 'rb') as f:
        zipped_code = f.read()
  
    role = iam.get_role(RoleName='LambdaBasicExecution')
    response = lambda_client.create_function(
        FunctionName=function_name,Runtime='python3.10',
        Role=role['Role']['Arn'],Handler='handler.lambda_handler',
        Code=dict(ZipFile=zipped_code),Timeout=300, 
        Environment={'Variables':{'Name':function_name,'Environment':'prod'}},
    )
    print(response)
    return response

def create_version(version_name):
    lambda_client = boto3.client('lambda')
    response = lambda_client.publish_version(FunctionName=version_name,)
    return response

def describe_function(function_name):
    lambda_client = boto3.client('lambda')
    response = lambda_client.get_function(FunctionName=function_name)
    print(response)
    return response

def invoke_function(function_name):
    lambda_client = boto3.client('lambda')
    test_event = dict()
    response = lambda_client.invoke(FunctionName=function_name,Payload=json.dumps(test_event),)
    print(response['Payload'])
    print(response['Payload'].read().decode("utf-8"))
    return response

def update_function(function_name,zip_file):
    lambda_client = boto3.client('lambda')
    with open(zip_file, 'rb') as f:
        zipped_code = f.read()
    response = lambda_client.update_function_code(FunctionName=function_name,ZipFile=zipped_code)
    print(response)

# describe_function('BooklinkUpload')
zip_file = archive_lambda(os.environ['HOME'] + '/lav/src/booklink/lambda/test/test_lambda')
update_function('BooklinkUpload',zip_file)

invoke_function('BooklinkUpload')
