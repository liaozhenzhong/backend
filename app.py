#!/usr/bin/env python3
import aws_cdk as cdk

from lib.dynamodb_stack import DynamoDBStack

app = cdk.App()
DynamoDBStack(app, "DynamoDBStack")

app.synth()
