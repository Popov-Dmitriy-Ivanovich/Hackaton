
import vk
from collections import Counter
import pandas as pd
import time



def get_members(groupid): # Получаем первую 10000 подписчиков
    first = vk_api.groups.getMembers(group_id=groupid, v=5.92)
    data = first["items"]

    count = first["count"] // 10000000



    for i in range(1, count+1):
        data = data + vk_api.groups.getMembers(group_id=groupid, v=5.92, offset=i*10)["items"]
    return data

def save_user_data(data, filename): # Сохраняем айдишники пользователей
    with open(filename, "w") as file:
        for item in data:
            file.write("vk.com/id" + str(item) + "\n")

def save_sub_data(data, filename): #Сохраняем паблики 
    with open(filename, "w") as file:
        for item in data:
            file.write("vk.com/" + str(item) + "\n")


def enter_user_data(filename): # Выводим пользователей
    with open(filename) as file:
        b = []

        for line in file:
            b.append(line[9:len(line) - 1])
    return b

def enter_sub_data(filename): # Выводим паблики
    with open(filename) as file:
        b = []
        for line in file:
            b.append(line[7:len(line) - 1])
    return b



def get_user_subscriptions(userid): # Получаем подписки пользователей
    try:
        response = vk_api.users.getSubscriptions(user_id=userid, v=5.92)
        subscriptions = response['groups']['items']
        return subscriptions
    except Exception as e:
        return None

def get_groups_info(groupid): #  Получаем информацию о группах
    try:
        response = vk_api.groups.getById(group_id=groupid, fields="description", v=5.92)
        name = response[0]['name']
        descr = response[0]['description']
        return name, descr
    except Exception as e:
        return None


def groupByName(data): #Получаем айдишник по названию
    try:
        response = vk_api.groups.getById(group_id=data, v=5.92)
        groupId = response[0]['id']
        return groupId
    except Exception as e:
        return None


def common_subs(data): # Выводим топ-10 пабликов
      all_subs_flat = [sub for sublist in data['subs'] for sub in sublist]
      subs_counter = Counter(all_subs_flat)
      top_subs_count = 10
      top_subs = subs_counter.most_common(top_subs_count)

      group_info = {'group_id': [], 'name': [], 'description': [], 'count': []}
      print(top_subs)
      for sub, count in top_subs:
        if get_groups_info(sub):
          name, description = get_groups_info(sub)
          time.sleep(3)
          group_info['group_id'].append(sub)
          group_info['name'].append(name)
          group_info['description'].append(description)
          group_info['count'].append(count)
      return pd.DataFrame(group_info)




def analyze_subs(members): # Собираем информацию о пабликах
    groups = {'user_id': [], 'subs': []}
    for i in members:
      user_subs = get_user_subscriptions(i)
      if user_subs:
        groups['user_id'].append(i)
        groups['subs'].append(user_subs)
    data = groups
    return data





if __name__ == "__main__":
    token = ""
    vk_api = vk.API(token)

    idgroup = groupByName('rare_plants_collection') 

    members = get_members(idgroup)
    save_user_data(members, str(idgroup)+".txt")
    data = analyze_subs(members)
    com = common_subs(data)

    print(com)
    com.to_csv('/content/drive/MyDrive/Buhgalt.csv')
