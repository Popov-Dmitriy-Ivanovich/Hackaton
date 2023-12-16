import vk
from collections import Counter
import pandas as pd
import time
import json


def get_members(groupid, token):  # Получаем первую 10000 подписчиков
    vk_api = vk.API(token)
    first = vk_api.groups.getMembers(group_id=groupid, v=5.92)
    data = first["items"]

    count = first["count"] // 10000000

    for i in range(1, count + 1):
        data = (
            data
            + vk_api.groups.getMembers(group_id=groupid, v=5.92, offset=i * 10)["items"]
        )
    return data


def save_user_data(data, filename):  # Сохраняем айдишники пользователей
    with open(filename, "w") as file:
        for item in data:
            file.write("vk.com/id" + str(item) + "\n")


def save_sub_data(data, filename):  # Сохраняем паблики
    with open(filename, "w") as file:
        for item in data:
            file.write("vk.com/" + str(item) + "\n")


def enter_user_data(filename):  # Выводим пользователей
    with open(filename) as file:
        b = []

        for line in file:
            b.append(line[9 : len(line) - 1])
    return b


def enter_sub_data(filename):  # Выводим паблики
    with open(filename) as file:
        b = []
        for line in file:
            b.append(line[7 : len(line) - 1])
    return b


def get_user_subscriptions(userid, token):  # Получаем подписки пользователей
    vk_api = vk.API(token)
    try:
        response = vk_api.users.getSubscriptions(user_id=userid, v=5.92)
        subscriptions = response["groups"]["items"][:15]
        print(subscriptions)
        return subscriptions
    except Exception as e:
        return None


def get_groups_info(groupid, token):  #  Получаем информацию о группах
    vk_api = vk.API(token)
    group_info = {"name": [], "description": []}
    try:
        response = vk_api.groups.getById(
            group_ids=groupid, fields="description", v=5.92
        )
        for i in response:
            group_info["name"].append(i["name"])
            group_info["description"].append(i["description"])

    except Exception as e:
        pass

    return group_info


def get_groups_info_execute(group_ids, token):  # неактуально, но возможно пригодится
    print(group_ids)
    vk_api = vk.API(token)
    code = """
        var result = [];
       
        %s.forEach(function(groupId){
            var info = API.groups.getById(
                {
                    {group_ids: groupId,
                    fields: "description"}
                    });
            result.push(info[0]);
            console.log(info);
        });
        
        return result;"""

    try:
        code = code % json.dumps(group_ids)  # вместо %s подставит group_ids
        print(
            vk_api.execute(code)
        )  # TypeError: APIMethod.__call__() takes 1 positional argument but 2 were given
        response = vk_api.execute(code)
        return [(item["name"], item["description"]) for item in response]
    except Exception as e:
        return []


def groupByName(data, token):  # Получаем айдишник по названию
    vk_api = vk.API(token)
    try:
        response = vk_api.groups.getById(group_id=data, v=5.92)
        groupId = response[0]["id"]
        return groupId
    except Exception as e:
        return None


def common_subs(data, token):  # Выводим топ-10 пабликов
    all_subs_flat = [sub for sublist in data["subs"] for sub in sublist]
    subs_counter = Counter(all_subs_flat)
    top_subs_count = 10
    top_subs = subs_counter.most_common(top_subs_count)

    group_info = {"group_id": [], "name": [], "description": [], "count": []}
    print(top_subs)
    for sub, count in top_subs:
        if get_groups_info(sub):
            name, description = get_groups_info(sub, token)
            time.sleep(3)
            group_info["group_id"].append(sub)
            group_info["name"].append(name)
            group_info["description"].append(description)
            group_info["count"].append(count)
    return pd.DataFrame(group_info)


def analyze_subs(members, token):  # Собираем информацию о пабликах
    groups = {"user_id": [], "subs": []}
    for i in members:
        user_subs = get_user_subscriptions(i, token)
        if user_subs:
            groups["user_id"].append(i)
            groups["subs"].append(user_subs)
    data = groups
    return data


# Получаем данные из вконтакте


def get_vk_data(token):
    vk_api = vk.API(token)

    dict = {
        "Паблик": "public",
    }

    for con in dict:
        res = dict[con]
        idgroup = groupByName(res, token)

        members = get_members(idgroup, token)
        data = analyze_subs(members, token)
        com = common_subs(data, token)

        print(com)
        com.to_csv(
            "/professions/Science/" + con + ".csv",
            mode="a",
            header=False,
            index=False,
        )
