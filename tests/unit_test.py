from datetime import datetime, timedelta
import json
import hashlib
import os

import awswrangler as wr
import pytest
import pytest_mock
import moto

from src.app import write_to_dynamodb

# assert that the item was written to dynamodb, and that the hash PK is properly 32 characters long
def test_write_to_dynamodb(moto_dynamodb, faker, aws_credentials):
    table_name = "jacobs_pytest_table"
    name_hash = write_to_dynamodb(faker, table_name)
    table = wr.dynamodb.get_table(table_name=table_name)
    response = table.get_item(
        Key={
            'name_hash_pk': f'{name_hash}'
        }
    )
    assert ['name_hash_pk', 'name', 'scrape_ts'] == list(response['Item'].keys())
    assert table.item_count == 1
    assert len(response['Item']['name_hash_pk']) == 32
    assert os.environ.get("test") == "test456"
