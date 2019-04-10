from chalice import Chalice
from chalicelib import db
from chalicelib import auth
from chalice import AuthResponse
import os
import boto3

app = Chalice(app_name='mytodo')
app.debug = True
_DB = None
_USER_DB = None

## Initialize the DB
def get_app_db():
    global _DB
    if _DB is None:
        ## Choose InMemoryTodoDB for non persistence
        ## For persistence choose DynamoDBTodo
        #_DB = db.InMemoryTodoDB()
        print boto3.resource('dynamodb').Table(os.environ['APP_TABLE_NAME'])
        _DB = db.DynamoDBTodo(
            boto3.resource('dynamodb').Table(
                os.environ['APP_TABLE_NAME'])
        )
    return _DB

def get_users_db():
    global _USER_DB
    if _USER_DB is None:
        _USER_DB = boto3.resource('dynamodb').Table(
            os.environ['USERS_TABLE_NAME'])
    return _USER_DB

## Make sure this method is in the start, so that the app understands that we intent to use authorization
@app.authorizer()
def jwt_auth(auth_request):
    token = auth_request.token
    decoded = auth.decode_jwt_token(token)
    return AuthResponse(routes=['*'], principal_id=decoded['sub'])

@app.route('/todos', methods=['GET'],authorizer=jwt_auth)
def get_todos():
    return get_app_db().list_items()


@app.route('/todos', methods=['POST'],authorizer=jwt_auth)
def add_new_todo():
    body = app.current_request.json_body
    return get_app_db().add_item(
        description=body['description'],
        metadata=body.get('metadata'),
    )


@app.route('/todos/{uid}', methods=['GET'],authorizer=jwt_auth)
def get_todo(uid):
    return get_app_db().get_item(uid)


@app.route('/todos/{uid}', methods=['DELETE'],authorizer=jwt_auth)
def delete_todo(uid):
    return get_app_db().delete_item(uid)


@app.route('/todos/{uid}', methods=['PUT'],authorizer=jwt_auth)
def update_todo(uid):
    body = app.current_request.json_body
    get_app_db().update_item(
        uid,
        description=body.get('description'),
        state=body.get('state'),
        metadata=body.get('metadata'))
    return "Updated Successfully"

@app.route('/test-ddb')
def test_ddb():
    resource = boto3.resource('dynamodb')
    ## Get the table name from the config.json
    table = resource.Table(os.environ['APP_TABLE_NAME'])
    return table.name

@app.route('/login', methods=['POST'])
def login():
    body = app.current_request.json_body
    record = get_users_db().get_item(
        Key={'username': body['username']})['Item']
    ## Generate the JWT token-- More analysis needed on the code
    jwt_token = auth.get_jwt_token(
        body['username'], body['password'], record)
    return {'token': jwt_token}

