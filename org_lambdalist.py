#this code is provided as-is with no warranty

import boto3
import botocore

#################################
#Setup
#   1. Create a role in your main organzation account to be used to run this code.
#      The role can be named anything and needs to contain the following policy:
#{
#    "Version": "2012-10-17",
#    "Statement": [
#        {
#            "Effect": "Allow",
#            "Action": "sts:AssumeRole",
#            "Resource": "arn:aws:iam::*:role/*"
#        }
#    ]
#}
#
#      If you use a different role name, please update the ARN listed above.
#
#   2. This role should be attached to Cloud9 instance.  Cloud9 is a good solution 
#      for this, as it already includes the boto3 library installed.  EC2 can also be
#      used.
#
#   3.  Create a role in each of your Organizations accounts named 'lambda_lister' and
#       attach the following policy to the role:
#
#{
#    "Version": "2012-10-17",
#    "Statement": [
#        {
#            "Effect": "Allow",
#            "Action": "lambda:ListFunctions",
#            "Resource": "*"
#        }
#    ]
#}
#
#       This role needs to allow the account you are running this from, e.g. your 
#       main organization account, to assume this role.
#
#       See https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html 
#       for information on how to setup a role to be assumed by an account.



orgs = boto3.client('organizations')
lambdacli = boto3.client('lambda')
sts = boto3.client('sts')

#modify this for the regions to check
regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']

#modify this to check for different runtimes
runtimes = ['nodejs6.10','dotnetcore2.0']

#modify this line to be the specific role that is setup in your organization
roletemplate = 'arn:aws:iam::{}:role/lambda_lister'




accounts = orgs.list_accounts(MaxResults=5)
x = True
print('Checking Org accounts')

for account in accounts['Accounts']:
    print('Checking account # {}').format(account['Id'])
    ###assume role in each account
    rolearn = 'arn:aws:iam::{}:role/lambda_lister'.format(account['Id'])
    print(rolearn)
    sts_response = sts.assume_role(RoleArn=rolearn,RoleSessionName=account['Id'])
    # From the response that contains the assumed role, get the temporary 
    # credentials that can be used to make subsequent API calls
    credentials=sts_response['Credentials']

    # Use the temporary credentials that AssumeRole returns to make a 
    # connection to Amazon S3  
    lambdacli=boto3.client(
        'lambda',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    response = lambdacli.list_functions() 
    for lambda_function in response['Functions']:
        if(lambda_function['Runtime']) in runtimes:
            arn_split = lambda_function['FunctionArn'].split(':')
            region=arn_split[3]
            print('{} in account {} and region {} is running {}').format(lambda_function['FunctionName'], account['Id'], region, lambda_function['Runtime']) 
