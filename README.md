# lambda_lister #

This python script can be run in an Organization account and will identify Lambdas that use a specific runtime in defined regions.

## Regions ## 
Modify this line to adjust the regions to check for Lambda functions in

`regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']`

## Runtimes ##
Modify this line to adjust the runtimes to look for

`runtimes = ['nodejs6.10','dotnetcore2.0']`

## Assumed Role ##
Modify this line to identify the role to assume in your sub-accounts

`roletemplate = 'arn:aws:iam::{}:role/lambda_lister'`

## Execution ##
python org_lambdalist.py
