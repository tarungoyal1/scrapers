from pymongo import MongoClient


def get_urls():
    client = MongoClient()
    db = client['books']
    col_bookurls = db['book_urls']
    url_list = []
    batch_size = 1000
    while 1:
        cursor = col_bookurls.find(filter={'status': 'pending'}).limit(batch_size)
        for item in cursor:
            url_list.append(item['url'])
        yield url_list

def get_listurl():
    # it just send 1 0my_start_urlst urls which is enough, because they follow pagination
    client = MongoClient()
    db = client['books']
    col_list_urls = db['list_urls']
    url_list = []
    while 1:
        cursor = col_list_urls.find(filter={'status': 'pending'}).limit(1)
        for item in cursor:
            url_list.append(item['list_url'])
        yield url_list

def updateListStatus(list_url):
    client = MongoClient()
    db = client['books']
    col_list_urls = db['list_urls']
    updateResult = col_list_urls.update_one({'list_url': list_url}, {'$set': {'status': 'done'}},upsert=False).modified_count
    if updateResult ==1:
        return True
    return False

if __name__ == '__main__':
    pass