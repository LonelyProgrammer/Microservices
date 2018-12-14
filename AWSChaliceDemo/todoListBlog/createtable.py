import os
import uuid
import json
import argparse

import boto3


TABLES = {
    'app': {
        'prefix': 'todo-app',
        'env_var': 'APP_TABLE_NAME',
        'hash_key': 'username',
        'range_key': 'uid'
    },
    'users': {
        'prefix': 'users-app',
        'env_var': 'USERS_TABLE_NAME',
        'hash_key': 'username',
    }
}


def create_table(table_name_prefix, hash_key, range_key=None):
    table_name = '%s-%s' % (table_name_prefix, str(uuid.uuid4()))
    client = boto3.client('dynamodb')
    ## For more information on Dynamo DB attributes nd key schema see - https://gist.github.com/jlafon/d8f91086e3d00c4bff3b
    key_schema = [
        {
            'AttributeName': hash_key,
            'KeyType': 'HASH',## DynamoDB supports two types of primary keys, a Hash Key and a Hash and Range Key
        }
    ]
    attribute_definitions = [
        {
            'AttributeName': hash_key,
            'AttributeType': 'S', ## This means that the attribute is type string
        }
    ]
    ## Check if Range key is provided or not
    if range_key is not None:
        key_schema.append({'AttributeName': range_key, 'KeyType': 'RANGE'})
        attribute_definitions.append(
            {'AttributeName': range_key, 'AttributeType': 'S'})
    client.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ##Amazon DynamoDB has two read/write capacity modes for processing reads and writes tables
        ## On-demand and Provisioned (Free) so I use ProvisionedThroughput
        ## throughput capacity in terms of read capacity units (RCUs) and write capacity units (WCUs)
        ## One read capacity unit represents one strongly consistent read per second, 
        ##or two eventually consistent reads per second, for an item up to 4 KB in size
        ##For example, if your item size is 8 KB, you require 2 read capacity units to sustain one strongly consistent read per second, 
        ##1 read capacity unit if you choose eventually consistent reads
        ##One write capacity unit represents one write per second for an item up to 1 KB in size.
        ##For example, if your item size is 2 KB, you require 2 write capacity units to sustain one write request per second 
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    )
    waiter = client.get_waiter('table_exists')
    ##wait argument specifies that we would like the function to block until the table is ready.
    waiter.wait(TableName=table_name, WaiterConfig={'Delay': 1})
    return table_name


def record_as_env_var(key, value, stage):
    with open(os.path.join('.chalice', 'config.json')) as f:
        data = json.load(f)
        data['stages'].setdefault(stage, {}).setdefault(
            'environment_variables', {}
        )[key] = value
    with open(os.path.join('.chalice', 'config.json'), 'w') as f:
        serialized = json.dumps(data, indent=2, separators=(',', ': '))
        f.write(serialized + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stage', default='dev')
    # app - stores the todo items
    # users - stores the user data.
    parser.add_argument('-t', '--table-type', default='app',
                        choices=['app', 'users'],
                        help='Specify which type to create')
    args = parser.parse_args()
    table_config = TABLES[args.table_type]
    table_name = create_table(
        table_config['prefix'], table_config['hash_key'],
        table_config.get('range_key')
    )
    record_as_env_var(table_config['env_var'], table_name, args.stage)


if __name__ == '__main__':
    main()