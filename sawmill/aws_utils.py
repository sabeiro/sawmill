"""
aws_utils: collection functions to interact with aws. More as a remainder of the function usage.

"""

import pandas as pd
import time
import boto3

def athena2pandas(result):
    '''transform athena results into a pandas data frame'''
    matrix = [[data.get('VarCharValue') for data in row['Data']] for row in result['ResultSet']['Rows']]
    df = pd.DataFrame(matrix[1:],columns=matrix[0])
    return df

def exec_athena(athena,query,params):
    """execute an athena query"""
    q_id = athena.start_query_execution(
        QueryString = query
        ,QueryExecutionContext = params['db']
        ,WorkGroup = params['group']
        #,ResultConfiguration = params['results']
    )
    status = 'RUNNING'
    for i in range(params['iteration']):
        resp = athena.get_query_execution(QueryExecutionId = q_id['QueryExecutionId'])
        status = resp['QueryExecution']['Status']['State']
        print(status)
        if (status == 'FAILED') or (status == 'CANCELLED'):
            print(resp['QueryExecution']['Status']['StateChangeReason'])
            return False
        elif status == 'SUCCEEDED':
            location = resp['QueryExecution']['ResultConfiguration']['OutputLocation']
            return location
            result = athena.get_query_results(QueryExecutionId = q_id['QueryExecutionId'])
            return location, result
        else:
            time.sleep(2)

def download_s3_subdir(bucketN,fileN,download_path):
    """download content of a subdirectory"""
    d = "/".join(fileN.split("/")[:-1]) + "/"
    buck = s3_resource.Bucket(bucketN)
    objects = buck.objects.filter(Prefix=d)
    for obj in objects:
        path, filename = os.path.split(obj.key)
        fName = "_".join(filename.split("/"))
        buck.download_file(obj.key, download_path + fName)


