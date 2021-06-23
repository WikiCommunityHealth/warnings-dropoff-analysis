from sys import argv
import gzip
from pymongo import MongoClient, UpdateOne
from json import loads
import os

def get_file_path(lang: str) -> str:
    for filename in os.listdir('wiki_lang'):
        if filename.startswith(f'{lang}') and filename.endswith('dataset.json.gz'):
            return f'wiki_lang/{filename}'
    return None

def get_users_collection(lang: str):
    client = MongoClient()
    users_collection = client.get_database('user_metrics').get_collection(f'{lang}wiki_users')
    return users_collection

def upload_lang(lang: str, file_path: str) -> None:
    print('Start updating users')
    with gzip.open(file_path, 'rt') as input:
        bulk_updates = []
        users_collection = get_users_collection(lang)
        a = 0
        for line in input:
            a += 1
            obj = loads(line.rstrip('\n'))
            username = obj['name'].split('/', 1)[0]
            languages = obj['languages']
            bulk_updates.append(UpdateOne({'username': username}, {'$set': {'languages': languages}}))
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
        print('Daaset file not found')
        exit(1)
    upload_lang(lang, path)