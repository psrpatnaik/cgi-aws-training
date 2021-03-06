from boto3 import client, resource
from botocore.credentials import InstanceMetadataProvider, InstanceMetadataFetcher

REGION_NAME = "us-east-1"

client = client('dynamodb',region_name = REGION_NAME)
resource = resource('dynamodb',region_name = REGION_NAME)# BookTable = DynamoDB.Table('Book')

'''
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table
    Create a new table
'''
def CreateATableBook():
        
    client.create_table(
        AttributeDefinitions = [ #array of attributes (name and type)
            {
                'AttributeName': 'id', # Name of the attribute
                'AttributeType': 'N'   # N -> Number (S -> String, B-> Binary)
            }
        ],
        TableName = 'Book', # Name of the table 
        KeySchema = [       # 
            {
                'AttributeName': 'id',
                'KeyType'      : 'HASH' # HASH -> partition key, RANGE -> sort key
            }
        ],
        BillingMode = 'PAY_PER_REQUEST',
        Tags = [ # OPTIONAL 
            {
                'Key' : 'test-resource',
                'Value': 'dynamodb-test'

            }
        ]
    )


'''
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_table
    Delete a table
'''


'''
    https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html
    CRUD Operations
'''
BookTable = resource.Table('Book')

def addItemToBook(id, title, author):

    response = BookTable.put_item(
        Item = {
            'id'     : id,
            'title'  : title,
            'author' : author,
            'likes'  : 0
        }
    )

    return response

def GetItemFromBook(id):

    response = BookTable.get_item(
        Key = {
            'id'     : id
        },
        AttributesToGet=[
            'title', 'author' # valid types dont throw error, 
                              # Other types should be converted to python type before sending as json response
        ]
    )

    return response

def UpdateItemInBook(id, data:dict):

    response = BookTable.update_item(
        Key = {
            'id': id
        },
        AttributeUpdates={
            'title': {
                'Value'  : data['title'],
                'Action' : 'PUT' # # available options -> DELETE(delete), PUT(set), ADD(increment)
            },
            'author': {
                'Value'  : data['author'],
                'Action' : 'PUT'
            }
        },
        ReturnValues = "UPDATED_NEW"  # returns the new updated values
    )
    return response

def LikeABook(id):

    response = BookTable.update_item(
        Key = {
            'id': id
        },
        AttributeUpdates = {
            'likes': {
                'Value'  : 1,
                'Action' : 'ADD'
            }
        },
        ReturnValues = "UPDATED_NEW"
    )
    response['Attributes']['likes'] = int(response['Attributes']['likes'])

    return response

def ModifyAuthorforBook(id, author):

    response = BookTable.update_item(
        Key = {
            'id': id
        },
        UpdateExpression = 'SET info.author = :new_author', #set author to new value
        #ConditionExpression = '', # execute until this condition fails # no condition
        ExpressionAttributeValues = { # Value for the variables used in the above expressions
            ':new_author': author
        },
        ReturnValues = "UPDATED_NEW"  #what to return
    )
    return response

def DeleteAnItemFromBook(id):

    response = BookTable.delete_item(
        Key = {
            'id': id
        }
    )

    return response
    
# batch get items resource
