import json
import boto3
import base64
import requests

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Extract and decode the Authorization header
    print(f'This is the event: {event}')
    auth_header = event['headers'].get('authorization')
    print(f'This is the auth header: {auth_header}')
    if not auth_header or not auth_header.startswith('Basic '):
        return {
            'statusCode': 401,
            'body': 'Missing or incorrect authentication header.'
        }
    table_name = 'staff-credentials'
    response = dynamodb.scan(TableName=table_name)
    items = response.get('Items', [])
    username_passwords = [f"{item['username']['S']}:{item['password']['S']}" for item in items]
    print(f'These are the username password pairs: {username_passwords}')
    encoded_user_pass = [f'Basic {base64.b64encode(item.encode()).decode()}' for item in username_passwords]
    print(f'These are the encoded username password pairs: {encoded_user_pass}')

    # Validate the credentials
    if auth_header not in encoded_user_pass:    # Later it must be replaced by environment variables
        return {
            'statusCode': 401,
            'body': 'Invalid credentials.'
        }

        # Extract and process data from the original request
    headers = event['headers']
    print(f'These are the headers: {headers}')
    request_type = event['requestContext']['http']['method']
    print(f"This is the request type: {request_type}")

    if request_type == 'POST' or request_type == 'PATCH':
        body = event['body']
    path = event['requestContext']['http']['path']

    print(f'This is the path: {path}')
    # Perform any necessary transformations or processing

    # Forward the request to API Gateway B
    # wind_hosp_api = '<https://7wn5vduzgd.execute-api.eu-west-2.amazonaws.com>' # Replace with the actual URL
    wind_hosp_api = '<http://d37nrc5ex7j0uo.cloudfront.net>'

    if request_type == 'POST' or request_type == 'PATCH':
        response = requests.post(f'{wind_hosp_api}{path}', headers=headers, data=body)
    else:
        print('Before GET')
        print(f'This is the request URL: {wind_hosp_api}{path}')
        response = requests.get(f'{wind_hosp_api}{path}', verify=False, headers=headers) # Research how to configure the requests library to accept HTTPS requests
        print('After GET')

    print(f'This is the response: {response.status_code}, {response.text}, {response.headers}')

    # Handle the response from API Gateway B
    # You can return the response from API Gateway B as the response to the original request
    # return {
    #     'statusCode': 200,
    #     'body': 'It works!',
    #     'headers': {}  # Convert headers to a standard dictionary
    # }

    return {
        'statusCode': response.status_code,
        'body': response.text,
        'headers': dict(response.headers)  # Convert headers to a standard dictionary
    }