import os
import json
import getpass
import argparse
import hashlib
import hmac

import boto3
from boto3.dynamodb.types import Binary


def get_table_name(stage):
    # We might want to user the chalice modules to
    # load the config.  For now we'll just load it directly.
    with open(os.path.join('.chalice', 'config.json')) as f:
        data = json.load(f)
    return data['stages'][stage]['environment_variables']['USERS_TABLE_NAME']


def create_user(stage):
    table_name = get_table_name(stage)
    ## Get the name of the table from the command line and asks Boto to create the table
    table = boto3.resource('dynamodb').Table(table_name)
    username = raw_input('Username: ').strip()
    ## Prompt the user for a value, usually a password, without echoing what they type to the console.
    ## Read more about this library at https://pymotw.com/2/getpass/
    password = getpass.getpass('Password: ').strip()
    ## Encodes the password with a random 16 digit OS generated Salt
    password_fields = encode_password(password)
    item = {
        'username': username,
        'hash': password_fields['hash'],
        ## Binary type attributes can store any binary data, 
        ## such as compressed text, encrypted data, or images.
        'salt': Binary(password_fields['salt']),
        'rounds': password_fields['rounds'],
        'hashed': Binary(password_fields['hashed']),
    }
    ## Insert username and password into table
    table.put_item(Item=item)


def encode_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    rounds = 100000

    hashed = hashlib.pbkdf2_hmac('sha256', password, salt, rounds)
    return {
        'hash': 'sha256',
        'salt': salt,
        'rounds': rounds,
        'hashed': hashed,
    }


def list_users(stage):
    table_name = get_table_name(stage)
    table = boto3.resource('dynamodb').Table(table_name)
    for item in table.scan()['Items']:
        print(item['username'])


def test_password(stage):
    username = raw_input('Username: ').strip()
    password = getpass.getpass('Password: ').strip()
    table_name = get_table_name(stage)
    table = boto3.resource('dynamodb').Table(table_name)
    item = table.get_item(Key={'username': username})['Item']
    ## We cannot decode the DB password and the user input password since the SHA algorithms are 
    ## One way algorithm, so I do the reverse I encode the user input password with the DB salt value
    ## And compare it with the encoded DB password
    encoded = encode_password(password, salt=item['salt'].value)
    ## HMAC stands for Keyed-Hashing for Message Authentication. 
    # It's a message authentication code obtained by running a 
    # cryptographic hash function (like MD5, SHA1, and SHA256) 
    # over the data (to be authenticated) and a shared secret key. 
    if hmac.compare_digest(encoded['hashed'], item['hashed'].value):
        print("Password verified.")
    else:
        print("Password verification failed.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create-user', action='store_true')
    parser.add_argument('-t', '--test-password', action='store_true')
    parser.add_argument('-s', '--stage', default='dev')
    parser.add_argument('-l', '--list-users', action='store_true')
    args = parser.parse_args()
    if args.create_user:
        create_user(args.stage)
    elif args.list_users:
        list_users(args.stage)
    elif args.test_password:
        test_password(args.stage)


if __name__ == '__main__':
    main()