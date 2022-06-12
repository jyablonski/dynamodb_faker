from datetime import datetime, timedelta
import os

import boto3
import pytest
import pytest_mock
import moto

from src.app import write_to_dynamodb

# Fixtures are created when first requested by a test, and are destroyed based on their scope:
# function: the default scope, the fixture is destroyed at the end of the test.
# class: the fixture is destroyed during teardown of the last test in the class.
# module: the fixture is destroyed during teardown of the last test in the module.
# package: the fixture is destroyed during teardown of the last test in the package.
# session: the fixture is destroyed at the end of the test session.


@pytest.fixture(scope="session")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'
    os.environ["test"] = "test456"


# Moto only works when two conditions are met:
# The logic to be tested is executed inside a Moto-context
# The Moto-context is started before any boto3-clients (or resources) are created
@pytest.fixture(scope="function")
def moto_dynamodb():
    with moto.mock_dynamodb():
        dynamodb = boto3.resource("dynamodb", region_name = "us-east-2")
        dynamodb.create_table(
            TableName="jacobs_pytest_table",
            KeySchema=[{"AttributeName": "name_hash_pk", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "name_hash_pk", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield dynamodb


# @pytest.fixture
# def faker_object():
#     fake = Faker()
#     return fake
