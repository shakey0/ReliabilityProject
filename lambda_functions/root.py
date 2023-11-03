import json
import secrets
import string

def lambda_handler(event, context):
    # Define a custom set of characters for your token
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
            <title>MedicalSystem</title>
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <meta name="csrf-param" content="authenticity_token" />
            <meta name="csrf-token"
                content="{csrf_token}" />
        </head>

        <body>
            Server is online.

        </body>

        </html>
        ''',
        'headers': {
            'Content-Type': 'text/html'
        }
    }