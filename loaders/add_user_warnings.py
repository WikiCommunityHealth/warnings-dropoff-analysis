from sys import argv
import gzip
from json import loads
from pymongo import MongoClient, UpdateOne
import os

def get_file_path(lang: str) -> str:
    for filename in os.listdir('wiki_warnings'):
        if filename.startswith(f'{lang}') and filename.endswith('dataset.json.gz'):
            return f'wiki_warnings/{filename}'
    return None

def get_users_collection(lang: str):
    client = MongoClient()
    users_collection = client.get_database('user_metrics').get_collection(f'{lang}wiki_users')
    return users_collection

def upload_user_warnings(lang: str, file_path: str) -> None:
    print('Start updating users')
    with gzip.open(file_path, 'rt') as input:
        bulk_updates = []
        users_collection = get_users_collection(lang)
        for line in input:
            obj = loads(line.rstrip('\n'))
            username = obj['name'].split('/', 1)[0]
            user_warnings_stats = obj['user_warnings_stats']
            user_warnings_recieved = obj['user_warnings_recieved']
            bulk_updates.append(UpdateOne({'username': username}, {'$set': {'user_warnings_stats': user_warnings_stats, 'user_warnings_recieved': user_warnings_recieved}}))
            if len(bulk_updates) > int(1.5e4):
                print('uploading...')
                users_collection.bulk_write(bulk_updates)
                bulk_updates = []
        users_collection.bulk_write(bulk_updates)
    print('Finished updating users')

if __name__ == '__main__':
    lang = argv[1]
    path = get_file_path(lang)
    if not path:
        print('Dataset file not found')
        exit(1)
    upload_user_warnings(lang, path)
