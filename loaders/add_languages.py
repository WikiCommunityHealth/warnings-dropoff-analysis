from sys import argv
from pymongo import MongoClient, UpdateOne
from json import loads

def get_file_path(lang: str) -> str:
    file_path = f'wiki_lang/{lang}wiki.json.gz'
    return file_path

def get_users_collection(lang: str):
    client = MongoClient()
    users_collection = client.get_database('user_metrics').get_collection(f'{lang}wiki_users')
    return users_collection

def upload_lang(lang: str, file_path: str) -> None:
    print('Start updating users')
    with open(file_path, 'r') as input:
        bulk_updates = []
        users_collection = get_users_collection(lang)
        for line in input:
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
    upload_lang(lang, path)