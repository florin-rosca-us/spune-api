import json
from pathlib import Path

# You can reference EFS files by including your local mount path, and then
# treat them like any other file. Local invokes may not work with this, however,
# as the file/folders may not be present in the container.
FILE = Path('/mnt/lambda/spune.json')

def lambda_get_handler(event, context):
    contents = None
    # The files in EFS are not only persistent across executions, but if multiple
    # Lambda functions are mounted to the same EFS file system, you can read and
    # write files from either function.
    try:
        with open(FILE, 'r') as f:
            contents = json.load(f)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(contents)
        }
    except Exception as e:
        errorMessage = 'Cannot load file: {}'.format(e)
        print(errorMessage)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': errorMessage})
        }

def lambda_put_handler(event, context):
    try:
        body = event.get('body')
        if body is None:
            raise Exception('Empty body')
        content = json.loads(body)
        print('Received JSON: {}'.format(json.dumps(content)))
        with open(FILE, 'w') as f:
            json.dump(content, f)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'saved': True # TODO: what else?
            }),
        }
    except Exception as e:
        errorMessage = 'Cannot save file: {}'.format(e)
        print(errorMessage)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': errorMessage})
        }
