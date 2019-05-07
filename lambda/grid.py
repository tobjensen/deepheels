import csv
import random

csv_file = 'shoes.csv'

with open(csv_file) as f:
	csv_reader = csv.DictReader(f)
	shoe_ids = [row['shoe_id'] for row in csv_reader]

def lambda_handler(event, context):
    print(event)
    
    grid_size = int(event['grid_size'])
    grid = random.sample(shoe_ids, k=grid_size)
    
    print(f'Grid: {grid}')
    return {
        'statusCode': 200,
        'grid': grid
    }