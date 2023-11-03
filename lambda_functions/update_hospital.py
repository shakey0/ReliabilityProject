import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    print(event)
    print(context)

    dynamodb = boto3.client('dynamodb')
    table_name = 'wind-hospitals'
    dynamodb_update = boto3.resource('dynamodb')
    table = dynamodb_update.Table(table_name)
    hospital_id = event['pathParameters']['id']
    body = event['body']
    hospital_name = json.loads(body)['name']

    print(hospital_name)
    print(type(hospital_name))

    primary_key = {
        'id': int(hospital_id)  # Adjust this to your table's primary key name and the desired value
    }

    updated_datetime = datetime.now()

    formatted_datetime = updated_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    # Update the item
    response = table.update_item(
        Key=primary_key,
        UpdateExpression='SET #nameAttribute = :newValue1, updated_at = :newValue2',
        ExpressionAttributeNames={
            '#nameAttribute': 'name'  # Alias for the reserved keyword "name"
        },
        ExpressionAttributeValues={
            ':newValue1': hospital_name,  # Adjust this as needed
            ':newValue2': formatted_datetime
        },

        ReturnValues="UPDATED_NEW")

    hospital_data = dynamodb.get_item(
        TableName='wind-hospitals',
        Key={
            'id': {
                'N': str(hospital_id)
            }
        }
    )
    print("data is here", hospital_data)

    # format hospital data to be returned to user
    def format_data(data):
        item = data.get('Item', {})
        return {
            'id': int(item.get('id', {}).get('N', 0)),
            'name': item.get('name', {}).get('S', ''),
            'created_at': item.get('created_at', {}).get('S', ''),
            'updated_at': item.get('updated_at', {}).get('S', ''),
            'url': f"<https://wind-reliability-server.animal-hospital.mkrs.link/hospitals/{item.get(>'id', {}).get('N', 0)}.json"
        }
    formatted_data = format_data(hospital_data)
    print("formatted data is here", formatted_data)

    # Convert items to a JSON file
    json_data = json.dumps(formatted_data, default=str, indent=4)

    return {
        'statusCode': 200,
        'body': json_data,
        'headers': {
            'Content-Type': 'application/json'
        }
    }