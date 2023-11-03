import json
import boto3
import string
import secrets

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('wind-hospitals')

    hospital_id = event['pathParameters']['id']

    response = table.delete_item(
        Key={
            'id': int(hospital_id)
        }
    )

    characters = string.ascii_letters + string.digits + string.punctuation  # includes letters, digits, and symbols

    # Generate a random token with a specific length
    token_length = 64  # You can adjust the length as needed
    csrf_token = ''.join(secrets.choice(characters) for x in range(token_length))

    print(event)

    return {
        'statusCode': 200,
        'body': f'''
        <!DOCTYPE html>
        <html>

        <head>
            <title>Hospital deleted</title>
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <meta name="csrf-param" content="authenticity_token" />
            <meta name="csrf-token"
                content="{csrf_token}" />
        </head>

        <body>
            The hospital with the id of {hospital_id} has been deleted.

        </body>

        </html>
        ''',
        'headers': {
            'Content-Type': 'text/html'
        }
    }