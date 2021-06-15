from sys import argv
from pymongo import MongoClient, UpdateOne

def get_file_path(lang: str) -> str:
    file_path = f'wiki_sex/{lang}.tsv'
    return file_path

def get_users_collection(lang: str):
    client = MongoClient()
    users_collection = client.get_database('user_metrics').get_collection(f'{lang}wiki_users')
    return users_collection

def upload_sex(lang: str, file_path: str) -> None:
    print('Start updating users')
    with open(file_path, 'r') as input:
        bulk_updates = []
        users_collection = get_users_collection(lang)
        for line in input:
            parts = line.split('\t')
            id = parts[0]
            try:
                sex = True if parts[2] == 'male' else (False if parts[2] == 'female' else None)
            except:
                print('Error in parsing sex', parts)
            bulk_updates.append(UpdateOne({'id': int(id)}, {'$set': {'sex': sex}}))
            if len(bulk_updates) > int(1.5e4):
                print('uploading')
                users_collection.bulk_write(bulk_updates)
                bulk_updates = []
        users_collection.bulk_write(bulk_updates)
    print('Finished updating users')

if __name__ == '__main__':
    lang = argv[1]
    path = get_file_path(lang)
    upload_sex(lang, path)