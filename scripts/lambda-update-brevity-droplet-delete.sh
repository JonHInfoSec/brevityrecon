#!/bin/bash
LAMBDANAME="brevity-droplet-delete"
PROJECT="brevityrecon"
mkdir /home/ec2-user/environment/$PROJECT/lambdas/build/$LAMBDANAME
cp -r /home/ec2-user/environment/$PROJECT/lib/* /home/ec2-user/environment/$PROJECT/lambdas/build/$LAMBDANAME
cp /home/ec2-user/environment/$PROJECT/lambdas/lambda_function_$LAMBDANAME.py /home/ec2-user/environment/$PROJECT/lambdas/build/$LAMBDANAME/lambda_function.py
cd /home/ec2-user/environment/$PROJECT/lambdas/build/$LAMBDANAME
zip -r ../$LAMBDANAME.zip *
aws s3 cp /home/ec2-user/environment/$PROJECT/lambdas/build/$LAMBDANAME.zip s3://brevity-deploy/infra/
aws lambda update-function-code --function-name $LAMBDANAME --s3-bucket brevity-deploy --s3-key infra/$LAMBDANAME.zip