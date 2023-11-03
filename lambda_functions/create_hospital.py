import json
import boto3
from datetime import datetime

def lambda_handler(event, context):

    dynamodb = boto3.client('dynamodb')
    table_name = 'wind-hospitals'
    response = dynamodb.scan(TableName=table_name)
    items = response.get('Items', [])

    def get_counter(items):
        return [int(item['hospital_counter']['N']) for item in items if item['id']['N'] == '0']

    last_id = get_counter(items)[0]
    dynamodb_update = boto3.resource('dynamodb')
    table = dynamodb_update.Table(table_name)
    primary_key = {
        'id': 0  # Adjust this to your table's primary key name and the desired value
    }

    # Update the item
    response = table.update_item(
        Key=primary_key,
        UpdateExpression='SET hospital_counter = :newValue',
        ExpressionAttributeValues={
            ':newValue': last_id+1  # Adjust this as needed
        },
        ReturnValues="UPDATED_NEW")

    print(response['Attributes'])

    body = json.loads(event['body'])

    # Get the name from the parsed body
    hospital_name = body.get('name')
    creation_datetime = datetime.now()
    formatted_datetime = creation_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    response = table.put_item(
       Item={
            'id': last_id+1,
            'name': hospital_name,
            'created_at': formatted_datetime,
            'updated_at': formatted_datetime,
        }
    )

    formatted_data = {
        'id': last_id+1,
        'name': hospital_name,
        'created_at': formatted_datetime,
        'updated_at': formatted_datetime,
        'url': f"https://wind-reliability-server.animal-hospital.mkrs.link/hospitals/{last_id+1}.json"
    }

    json_data = json.dumps(formatted_data, default=str, indent=4)

    return {
        'statusCode': 200,
        'body': json_data,
        'headers': {
            'Content-Type': 'application/json'
        }
    }