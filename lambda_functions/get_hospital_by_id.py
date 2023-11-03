import json
import boto3

client = boto3.client('dynamodb')
def lambda_handler(event, context):
    # retrieve hopsital id
    hospital_id = event['pathParameters']['id']
    print("hospital id is here", hospital_id)

    # retrieve hospital data from wind hospitals table
    hospital_data = client.get_item(
        TableName='wind-hospitals',
        Key={
            'id': {
                'N': str(hospital_id)
            }
        }
    )
    print("data is here", hospital_data)

    if 'Item' not in hospital_data:
        return {
            'statusCode': 404,
            'body': 'Hospital not found',
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    else:
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