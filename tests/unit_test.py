from datetime import datetime, timedelta
import os

import pytest
import pytest_mock
import moto

from src.app import *

# assert that the item was written to dynamodb, and that the hash PK is properly 32 characters long
def test_write_to_dynamodb(moto_dynamodb, faker, aws_credentials):
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'
    table_name = "jacobs_pytest_table"
    invoke = write_to_dynamodb(faker, table_name)
    table = wr.dynamodb.get_table(table_name=table_name)
    assert table.item_count == 1
    assert len(invoke) == 32
    assert os.environ.get("test") == "test456"
