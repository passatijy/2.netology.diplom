import vk_api
from pymongo import MongoClient
from datamongo import mk_mongodb, clear_db, find_by_name
import time


def univers_req(login, password):
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    return vk

def wall_get(login, password):
    """ Пример получения последнего сообщения со стены """

    #login, password = 'python@vk.com', 'mypassword'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    """ VkApi.method позволяет выполнять запросы к API. В этом примере
        используется метод wall.get (https://vk.com/dev/wall.get) с параметром
        count = 1, т.е. мы получаем один последний пост со стены текущего
        пользователя.
    """
    response = vk.wall.get(count=1)  # Используем метод wall.get

    if response['items']:
        print(response['items'][0])

def user_search(login, password, **search_param):
    resp = univers_req(login, password).users.search(**search_param)
    return resp

def user_search_cities(login, password, city, sex, age_to):
    for k in (city):
        search_result = []
        offset = input('Input offset: ')
        search_result = user_search(login, password,
            city=k, 
            count=80,
            sex=sex, 
            status='6', 
            age_from = '19',
            age_to = age_to, 
            has_photo='1',
            offset = offset
        )
        print('City:',k)
        long_user_list.append(search_result)
    return long_user_list

def users_get(login, password, user_id):
    result=[]
    temp_req = univers_req(login, password).users.get(user_ids=user_id)
    if (not temp_req[0]['is_closed']) or temp_req[0]['can_access_closed']:
        resp = univers_req(login, password).users.get(user_ids=user_id, 
            fields='bdate,sex,city,interests,books,music' )
        groups = univers_req(login, password).groups.get(user_id=user_id)
        friends = univers_req(login, password).friends.get(user_id=user_id)
        result.append(resp)
        result.append(groups)
        result.append(friends)
    else:
        print('User with id', user_id,'and name', resp[0]['first_name'], resp[0]['last_name'], 'have closed profile.')
    return result

def filling_base(db, collection, user_list):
    print('filling_base')
    for k in user_list:
        for n in k['items']:
            tmp_user = users_get(login, password, n['id'])
            tmp_user[0][0]['groups'] = tmp_user[1]
            tmp_user[0][0]['friends'] = tmp_user[2]
            db[collection].insert(tmp_user[0][0])
            print('user detail was get succesfully ')

def find_like_value(target_user_id, database, collection, match_field, field_weight):
    my_user_db = database[collection].find_one({'id': target_user_id})
    for user_doc in database[collection].find():
        #print(user_doc[match_field])
        counter = 0
        print('looking in user:', user_doc['first_name'],user_doc['last_name'])
        #print('target user ',match_field,' list:', my_user_db[match_field])
        for one_group in user_doc[match_field]['items']:
            # print('one_group', one_group)
            if one_group in my_user_db[match_field]['items']:
                counter +=1
                print('user group matched with target, counter: ', counter)
        if 'like_value' in user_doc.keys():
            like_calcul = user_doc['like_value'] + counter*field_weight
        else:
            like_calcul = counter*field_weight
        database.users_col.update_one({'id': user_doc['id']}, {'$set': {'like_value': like_calcul}})

def show_coll(db, collection):
    coll_size = 0
    for k in db[collection].find():
        coll_size += 1
        if 'like_value' in k.keys():
            print(k['id'],k['first_name'],k['last_name'],k['like_value'])
        else:
            print(k['id'],k['first_name'],k['last_name'])
    print('Collection size:', coll_size)



login = 'NetologyPythonVk@yandex.ru'

#my id: 552934290

if __name__ == '__main__':
# wall_get(login, password)
    client = MongoClient('localhost')
    dbnames = client.list_database_names()
    if 'users_db' in dbnames:
        work_db = client.users_db
        print('Database users_db found, checking collection users_col')
        if 'users_col' in client.users_db.collection_names():
            print('Collection users_col exist, ')
        else:
            print('Collection users_col not exist, creating')
            work_db.users_col
    else:
        print('db not found, creating')
        work_db = client.users_db
        work_db.users_col

    long_user_list = []
    long_user_list = user_search_cities(login, password, '1', '1', '35' )

# insert my own user in database:
    my_user = users_get(login, password, '552934290')
    my_user[0][0]['groups']=my_user[1]
    my_user[0][0]['friends']=my_user[2]
    work_db.users_col.insert(my_user[0][0])

    filling_base(work_db, 'users_col', long_user_list)

    show_coll(work_db, 'users_col')

    find_like_value(552934290, work_db, 'users_col', 'groups', 9)

    show_coll(work_db, 'users_col')

    find_like_value(552934290, work_db, 'users_col', 'friends', 11)

    show_coll(work_db, 'users_col')




