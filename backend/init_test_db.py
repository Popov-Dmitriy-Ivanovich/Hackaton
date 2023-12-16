import db.db_classes as db
import json
from db.db_classes import (
    connect_db,
    ProfessionsTable,
    CoursesTable,
    SingletonConnection,
)
from pydantic import BaseModel

TEST_ID = '189011945'
TEST_TOKEN = 'vk1.a.jQ-lueZqKIG1yx9aHBZEhqnWAT8MAOsu0xHgWxIsW2k0jqH74KqwKY0inb_SZKwYZ5bo-h08kxJ3dJxi5pn7e361ZSkhw0h9uIZ-W113Slsk_Gmoz6gCskg1PpSt0E7LvNqDl0mNSdQOpEzF1HOekA3wVUcnaOlT-Z2UUiK80FOJUfSWxYGYargPP4mqGax3'

class Profession:
    def __init__(self, name: str) -> None:
        self.name = name
        self.description = "description of profession: " + name


def clear_db(conn: SingletonConnection) -> None:
    users = conn.session.query(db.UsersTable).all()
    login = conn.session.query(db.LoginDataTable).all()
    cours = conn.session.query(db.CoursesTable).all()
    proff = conn.session.query(db.ProfessionsTable).all()
    favor = conn.session.query(db.FavouritesTable).all()
    for row in users:
        conn.session.delete(row)
    for row in login:
        conn.session.delete(row)
    for row in cours:
        conn.session.delete(row)
    for row in proff:
        conn.session.delete(row)
    for row in favor:
        conn.session.delete(row)
    conn.session.commit()


conn = connect_db()
clear_db(conn)

with open('analys/resourses/user_data.json','r', encoding='utf-8') as user_data_file:
    user_data = json.load(user_data_file)

proff = list(user_data.keys())
prof_data = list(map(lambda x: Profession(x), proff))
for i in prof_data:
    prof_unit = ProfessionsTable(name=i.name, description=i.description)
    conn.session.add(prof_unit)
    print(prof_unit.id)
    conn.session.commit()
    print(prof_unit.id)
    for i in range(3):
        course_unit = CoursesTable(
            course_name=f"course №{i} for profession {prof_unit.name}",
            description="some description for course",
            profession_id=prof_unit.id,
        )
        conn.session.add(course_unit)
        conn.session.commit()
        print(
            course_unit.course_name, course_unit.description, course_unit.profession_id
        )

users = [
    db.UsersTable(id=1 ,name='TestNoVKIDUser'),
    db.UsersTable(id=2, name='TestUser', vk_id='TestVKID'),
    db.UsersTable(id=3, name='TestUser', vk_id='TestVKID', access_token='TESTTOKEN'),
    db.UsersTable(id=4, name='TestUser', vk_id='TestVKID', access_token='TESTTOKEN'),
    db.UsersTable(id=5, name='TestUser', vk_id='TestVKID', access_token='TESTTOKEN'),
    db.UsersTable(id=6, name='TestUser', vk_id='TestVKID', access_token='TESTTOKEN'),
    db.UsersTable(id=7, name='TestVkIDUserNoFav', vk_id=TEST_ID, access_token=TEST_TOKEN),
    db.UsersTable(id=8, name='TestVkIDUserWithFav', vk_id=TEST_ID, access_token=TEST_TOKEN),
    db.UsersTable(id=9, name='TestUser', vk_id='TestVKID', access_token='TESTTOKEN'),
]
logins = [
    db.LoginDataTable(login='TestLogin1', password='TestPassword1', user_id=9),
    db.LoginDataTable(login='TestNoVkIDUser', password='TestPassword1', user_id=1),
    db.LoginDataTable(login='TestLogin2', password='TestPassword2', user_id=2),
    db.LoginDataTable(login='TestLogin3', password='TestPassword3', user_id=3),
    db.LoginDataTable(login='TestLogin4', password='TestPassword4', user_id=4),
    db.LoginDataTable(login='TestLogin5', password='TestPassword5', user_id=5),
    db.LoginDataTable(login='TestLogin6', password='TestPassword6', user_id=6),
    db.LoginDataTable(login='TestVkIdUserNoFav', password='TestPassword6', user_id=7),
    db.LoginDataTable(login='TestVkIdUserWithFav', password='TestPassword6', user_id=8),
]
for i in logins+users:
    conn.session.add(i)
    conn.session.commit()

conn.session.add(db.FavouritesTable(name='Образование',user_id = 8))
conn.session.add(db.FavouritesTable(name='Медицина и здравоохранение',user_id = 8))
conn.session.add(db.FavouritesTable(name='Сфера обслуживания',user_id = 8))
conn.session.add(db.FavouritesTable(name='Архитектура, строительство и недвижимость',user_id = 8))
# https://www.youtube.com/watch?v=jfgNz4s99IA
