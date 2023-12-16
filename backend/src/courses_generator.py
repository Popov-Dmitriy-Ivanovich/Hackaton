from pydantic import BaseModel
from db.db_classes import (
    connect_db,
    LoginDataTable,
    UsersTable,
    FavouritesTable,
    CoursesTable,
    ProfessionsTable,
)
from typing import List
from analys.analyze_user import UserAnaliser
import random


class CoursesRequestData(BaseModel):
    login: str


class CoursesRequest(BaseModel):
    data: CoursesRequestData


class CourseData(BaseModel):
    name: str
    description: str


class ProfessionData(BaseModel):
    name: str
    description: str


class ResponseData(BaseModel):
    courses: List[CourseData]
    professions: List[ProfessionData]


class RequestResponse(BaseModel):
    data: ResponseData


class CoursesGenerator:
    def __init__(self) -> None:
        self._connection = connect_db()

    def get_professions_and_courses_id(self, professions: list[str]):
        courses_ids = []
        prof_ids = []
        for prof in professions:
            prof_entity = (
                self._connection.session.query(ProfessionsTable)
                .filter_by(name=prof)
                .first()
            )
            if prof_entity == None:
                raise Exception(f"profession {prof} is not found in database")
            prof_ids.append(prof_entity.id)
        for i in prof_ids:
            courses_entities = (
                self._connection.session.query(CoursesTable)
                .filter_by(profession_id=i)
                .all()
            )
            for course in courses_entities:
                courses_ids.append(course.course_name)

        return (courses_ids, prof_ids)

    def guess_professions_by_login(self, login: str) -> list[str]:
        login_entity = (
            self._connection.session.query(LoginDataTable)
            .filter_by(login=login)
            .first()
        )
        if login_entity == None:
            raise Exception("login data not found")
        user_entity = (
            self._connection.session.query(UsersTable)
            .filter_by(id=login_entity.user_id)
            .first()
        )
        if user_entity == None:
            raise Exception("user data not found")
        favourites = self._get_user_favourites(user_entity.id)
        access_token = self._get_user_access_token(user_entity.id)
        vk_id = self._get_user_vk_id(user_entity.id)
        if vk_id == None:
            raise Exception("user has not logged in through VK")
        if access_token == None:
            raise Exception("User has no access token for some reason")
        return self.guess_professions(vk_id, access_token, favourites)

    def guess_professions(
        self, vk_id: str, access_token: str, favourites: list[str]
    ) -> list[str]:
        handler = UserAnaliser(vk_id, access_token, favourites)
        return handler.get_user_professions()

    def _get_user_favourites(self, user_id: int) -> list[str]:
        professions_entity = (
            self._connection.session.query(FavouritesTable)
            .filter_by(user_id=user_id)
            .all()
        )
        return list(map(lambda x: x.name, professions_entity))

    def _get_user_vk_id(self, user_id: int):
        return (
            self._connection.session.query(UsersTable)
            .filter_by(id=user_id)
            .first()
            .vk_id
        )

    def _get_user_access_token(self, user_id: int):
        return (
            self._connection.session.query(UsersTable)
            .filter_by(id=user_id)
            .first()
            .access_token
        )

    def execute(self, login: str):
        professions = self.guess_professions_by_login(login)
        cour_names, prof_ids = self.get_professions_and_courses_id(professions)
        prof_data = []
        cour_data = []
        for id in prof_ids:
            prof_entity = (
                self._connection.session.query(ProfessionsTable)
                .filter_by(id=id)
                .first()
            )
            if prof_entity == None:
                raise Exception("I hope that never happens")
            prof_data.append(
                ProfessionData(
                    name=prof_entity.name, description=prof_entity.description
                )
            )

        for name in cour_names:
            cour_entity = (
                self._connection.session.query(CoursesTable)
                .filter_by(course_name=name)
                .first()
            )
            if prof_entity == None:
                raise Exception("I hope that never happens")
            cour_data.append(
                CourseData(
                    name=cour_entity.course_name, description=cour_entity.description
                )
            )
        print(prof_data)
        print(cour_data)
        return RequestResponse(
            data=ResponseData(professions=prof_data, courses=cour_data)
        )


def get_courses(login):
    handler = CoursesGenerator()
    return handler.execute(login)
