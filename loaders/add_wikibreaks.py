from sys import argv
import gzip
from json import loads
from pymongo import MongoClient, UpdateOne

def get_file_path(lang: str) -> str:
    file_path = f'wiki_breaks/{lang}wiki.json.gz'
    return file_path

def get_users_collection(lang: str):
    client = MongoClient()
    users_collection = client.get_database('user_metrics').get_collection(f'{lang}wiki_users')
    return users_collection

def upload_wikibreaks(lang: str, file_path: str) -> None:
    print('Start updating users')
    print('Path {}'.format(file_path))
    with gzip.open(file_path, 'rt') as input:
        bulk_updates = []
        users_collection = get_users_collection(lang)
        for line in input:
            obj = loads(line.rstrip('\n'))
            username = obj['name'].split('/', 1)[0]
            wikibreaks = obj['wikibreaks']
            bulk_updates.append(UpdateOne({'username': username}, {'$set': {'wikibreaks': wikibreaks}}))
            if len(bulk_updates) > int(1.5e4):
                print('uploading...')
                users_collection.bulk_write(bulk_updates)
                bulk_updates = []
    print('Finished updating users')

if __name__ == '__main__':
    lang = argv[1]
    path = get_file_path(lang)
    upload_wikibreaks(lang, path)