import random
import boto3

table_name = 'deepheels'
aws_region = 'us-east-1'

table = boto3.resource('dynamodb', region_name=aws_region).Table(table_name)

def lambda_handler(event, context):
    print(event)
    
    like = str(event['like'])
    liked = event['liked']
    grid = event['grid']
    
    changes = []
    
    response = table.get_item( Key={'id': like} )
    similar_items = response['Item']['items']
    
    open_spots = [i for i in range(len(grid)) if grid[i] not in similar_items and grid[i] not in liked]
    print(f'Open spots: {open_spots}')
    
    new_items = [item for item in similar_items if item not in grid and item not in liked]
    print(f'New items: {new_items}')

    
    swap_positions = random.sample(open_spots, min(2, len(open_spots), len(new_items)))
    for position in swap_positions:
        item_id = new_items.pop()
        changes.append({'position':position, 'id':item_id})
        print(f'Replace {grid[position]} at position {position} with {item_id}')
        grid[position] = item_id

    print('New grid:', grid)

    return {
        'statusCode': 200,
        'changes': changes
    }
