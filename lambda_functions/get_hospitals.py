import json
import boto3
import base64

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    table_name = 'wind-hospitals'
    response = dynamodb.scan(TableName=table_name)
    items = response.get('Items', [])

    # Print the items to the logs for inspection
    print("Items from DynamoDB:", items)

    if not items:
        return {
            'statusCode': 200,
            'body': json.dumps("No items found in DynamoDB table")
        }

    def format_data(items):
        return [{
            'id':int(item['id']['N']),
            'name':item['name']['S'],
            'created_at':item['created_at']['S'],
            'updated_at':item['updated_at']['S'],
            'url':f"<https://wind-reliability-server.animal-hospital.mkrs.link/hospitals/{item[>'id']['N']}.json"
        } for item in items if item['id']['N'] != '0']


    formatted_data = format_data(items)
    formatted_data.sort(key=lambda x: x['id'], reverse=True)

    # Convert items to a JSON file
    json_data = json.dumps(formatted_data, default=str, indent=4)

    return {
        'statusCode': 200,
        'body': json_data,
        'headers': {
            'Content-Type': 'application/json'
        }
    }