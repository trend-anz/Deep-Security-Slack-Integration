# Deep Security Slack Integration

# Setup
## Slack

1. Create a Slack WorkSpace
2. Create a channel where you'd like the messages to be sent
2. Create a Slack App. Then inside the app:
	1. Create a bot user
	2. Give the app permissions to send messages
	3. Install the app in your workspace
	4. Record the `Bot User OAuth Access Token`


## AWS & Deep Security

1. Create an S3 bucket which will be used to store your Lambda.
2. Zip & upload the Lambda:

```
cd code
pip3 install -r requirements.txt --target ./package
cd package
zip -r9 ../ds-slack.zip .
cd ..
zip -g ds-slack.zip ds-slack.py
aws s3 cp ds-slack.zip s3://<LAMBDA_BUCKET_NAME>/<S3_KEY_PATH>/ds-slack.zip
``` 

3. (Optional) Validate the template:

```
cd ../cfn
aws cloudformation validate-template --template-body file://cfn.yaml
```

4. Run the template:

```
aws cloudformation create-stack \
--stack-name ds-slack-lambda \
--template-body file://cfn.yaml \
--parameters \
ParameterKey=LambdaBucketName,ParameterValue=<BUCKET_NAME> \
ParameterKey=LambdaS3KeyPath,ParameterValue=<S3_KEY_PATH> \
ParameterKey=SlackChannelName,ParameterValue=<SLACK_CHANNEL_NAME> \
ParameterKey=SlackApiToken,ParameterValue=<BOT_TOKEN> \
--capabilities CAPABILITY_IAM
```

5. [Configure Deep Security](https://help.deepsecurity.trendmicro.com/sns.html) to send SNS notifications.

# Dev Notes
## Update Lambda

If you update the code, you'll need to update Lambda:

```
aws lambda update-function-code \
    --function-name ds-slack \
    --s3-bucket <BUCKET_NAME> \
    --s3-key <S3_KEY_PATH>/ds-slack.zip
```