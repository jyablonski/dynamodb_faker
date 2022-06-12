from datetime import datetime
import hashlib
import json
import os
import time

import awswrangler as wr
from faker import Faker
import pandas as pd

# quick script to store fake data to dynamodb every 5 seconds
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
def write_to_dynamodb(faker_obj: Faker, dynamo_table: str):
    name = faker_obj.name()
    scrape_ts = datetime.now()
    name_hash_pk = hashlib.md5((name + str(scrape_ts)).encode("utf-8")).hexdigest()

    # hash concat with current timestamp for pk bc there might be 2 ppl who have the same exact name
    dynamo_payload = {
        "name_hash_pk": name_hash_pk,
        "name": name,
        "scrape_ts": scrape_ts,
    }

    # first dump then loads - have to convert datetime obj to string then load everything back to dict
    # in order to store the timestamps to dynamodb as a string
    wr.dynamodb.put_items(
        items=[json.loads(json.dumps(dynamo_payload, default=str))],
        table_name=dynamo_table,
    )
    print(f"Storing {name} to dynamodb table {dynamo_table} at {scrape_ts}")
    return name_hash_pk


fake = Faker()
starttime = time.time()
invocations = 0

while True:
    # this will loop for 14 seconds and then break
    # invoke at 0s, 5s, 10s, but not at 15s bc im breaking it beforehand.
    if time.time() > starttime + 14:
        print(f"Breaking Execution after {invocations} invocations")
        # print(f"printing {os.environ.get('test')}")
        break
    else:
        invoke = write_to_dynamodb(fake, "jacob_test_table")
        invocations += 1
        time.sleep(
            5 - ((time.time() - starttime) % 5)
        )  # triggers once when the program starts, then every 5 seconds after
        # time.sleep(5 - time.time() % 5)
