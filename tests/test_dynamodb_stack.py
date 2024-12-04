import pytest
from aws_cdk import App
from aws_cdk.assertions import Template, Match

from lib.dynamodb_stack import DynamoDBStack

@pytest.fixture(name='template_fixture')
def create_template_fixture():
    app = App()
    stack = DynamoDBStack(app, "TestDynamoDBStack")
    return Template.from_stack(stack)

def test_tracker_table_created(template_fixture):
    template_fixture.has_resource("AWS::DynamoDB::Table", {
        "Properties": {
            "KeySchema": [
                {
                    "AttributeName": "tracker_id",
                    "KeyType": "HASH"
                }
            ],
            "AttributeDefinitions": [
                {
                    "AttributeName": "tracker_id",
                    "AttributeType": "S"
                }
            ],
            "BillingMode": "PAY_PER_REQUEST",
            "PointInTimeRecoverySpecification": {
                "PointInTimeRecoveryEnabled": True
            }
        }
    })

def test_location_table_created(template_fixture):
    template_fixture.has_resource("AWS::DynamoDB::Table", {
        "Properties": {
            "KeySchema": [
                {
                    "AttributeName": "tracker_id",
                    "KeyType": "HASH"
                },
                {
                    "AttributeName": "timestamp",
                    "KeyType": "RANGE"
                }
            ],
            "AttributeDefinitions": [
                {
                    "AttributeName": "tracker_id",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "timestamp",
                    "AttributeType": "S"
                }
            ],
            "BillingMode": "PAY_PER_REQUEST",
            "TimeToLiveSpecification": {
                "AttributeName": "ttl",
                "Enabled": True
            },
            "PointInTimeRecoverySpecification": {
                "PointInTimeRecoveryEnabled": True
            }
        }
    })

def test_user_table_created(template_fixture):
    template_fixture.has_resource("AWS::DynamoDB::Table", {
        "Properties": {
            "KeySchema": [
                {
                    "AttributeName": "user_id",
                    "KeyType": "HASH"
                }
            ],
            "AttributeDefinitions": Match.array_with([
                {
                    "AttributeName": "user_id",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "email",
                    "AttributeType": "S"
                }
            ]),
            "BillingMode": "PAY_PER_REQUEST",
            "GlobalSecondaryIndexes": [
                {
                    "IndexName": "EmailIndex",
                    "KeySchema": [
                        {
                            "AttributeName": "email",
                            "KeyType": "HASH"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                }
            ],
            "PointInTimeRecoverySpecification": {
                "PointInTimeRecoveryEnabled": True
            }
        }
    })

def test_table_count(template_fixture):
    template_fixture.resource_count_is("AWS::DynamoDB::Table", 3)

def test_removal_policy(template_fixture):
    # Verify all tables have DESTROY removal policy (for non-production)
    tables = template_fixture.find_resources("AWS::DynamoDB::Table")
    for table in tables.values():
        assert table["DeletionPolicy"] == "Delete"  # nosec B101
