import vk_api


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

login = 'NetologyPythonVk@yandex.ru'
password = 'dogsheart'

if __name__ == '__main__':
# wall_get(login, password)
    long_user_list = []
    for k in ('1','2','3'):
        search_result = []
        search_result = user_search(login, password,
            city=k, 
            sex='1', 
            status='1', 
            age_from = '19', 
            age_to = '28', 
            has_photo='1')
        long_user_list.append(search_result)

    for k in long_user_list:
        print(' --------City ', k)
        for n in k['items']:
            print('Id: ', n['id'], ' First Name: ', n['first_name'], ' Last Name: ', n['last_name'])
