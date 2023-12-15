from requests import request
from db.db_classes import connect_db, LoginDataTable, UsersTable, FavouritesTable
import unittest

URL = "http://localhost:8000"


class TestMainFeatures(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self._conn = connect_db()
        super().__init__(methodName)

    def test_profile_form_process(self):
        req_body = {
            "login": "TestLogin5",
            "choises": [
                "Медицина и здравоохранение",
                "Искусство и развлечения",
                "Наука и образование",
                "Информационные технологии и программирование",
            ],
        }

        resp = request("post", URL + "/api/profile_form_res", json=req_body)

        with self.subTest(msg="assert response status"):
            self.assertEqual(resp.json(), {"status": "OK"})

        with self.subTest(msg="assert adding data to database"):
            user_instance = (
                self._conn.session.query(UsersTable)
                .filter_by(
                    id=self._conn.session.query(LoginDataTable)
                    .filter_by(login=req_body["login"])
                    .first()
                    .user_id
                )
                .first()
            )
            self.assertNotEqual(user_instance, None)
            favourites_instances = (
                self._conn.session.query(FavouritesTable)
                .filter_by(user_id=user_instance.id)
                .all()
            )
            for instance in favourites_instances:
                self.assertTrue(instance.name in req_body["choises"])

    def test_empty_profile_form_process(self):
        req_body = {"login": "TestLogin4", "choises": []}

        resp = request("post", URL + "/api/profile_form_res", json=req_body)

        with self.subTest(msg="assert response status"):
            self.assertEqual(resp.json(), {"status": "OK"})

        with self.subTest(msg="assert adding data to database"):
            user_instance = (
                self._conn.session.query(UsersTable)
                .filter_by(
                    id=self._conn.session.query(LoginDataTable)
                    .filter_by(login=req_body["login"])
                    .first()
                    .user_id
                )
                .first()
            )
            self.assertNotEqual(user_instance, None)
            favourites_instances = (
                self._conn.session.query(FavouritesTable)
                .filter_by(user_id=user_instance.id)
                .all()
            )
            for instance in favourites_instances:
                self.assertTrue(instance.name in req_body["choises"])

    def test_course_generator(self):
        # не возращает ошибку если аккаунт ВК привязан
        # возращает ошибку если аккаунт ВК не привязан
        # работает независимо от прохождения пользователем формы
        # в результате есть хотябы одна профессия и хотябы один курс
        corr_login_no_form = "TestLogin4"
        corr_login_with_form = "TestLogin5"
        wrong_login = "TestLogin1"
        print(
            request(
                "post",
                URL + "/api/get_courses",
                json={"data": {"login": corr_login_no_form}},
            ).json()
        )
        corr_login_no_form_resp = request(
            "post",
            URL + "/api/get_courses",
            json={"data": {"login": corr_login_no_form}},
        ).json()["data"]
        corr_login_with_form_resp = request(
            "post",
            URL + "/api/get_courses",
            json={"data": {"login": corr_login_with_form}},
        ).json()["data"]
        wrong_login_resp = request(
            "post", URL + "/api/get_courses", json={"data": {"login": wrong_login}}
        ).json()

        with self.subTest(msg="assert error response when VK is not authorized"):
            self.assertEqual(
                wrong_login_resp, {"err": "user has not logged in through VK"}
            )
        with self.subTest(msg="assert no error when VK is authorized"):
            self.assertTrue("err" not in corr_login_no_form_resp.keys())
            self.assertTrue("err" not in corr_login_with_form_resp.keys())
        with self.subTest(msg="assert response has professions inside"):
            self.assertTrue("professions" in corr_login_no_form_resp.keys())
            self.assertTrue("professions" in corr_login_with_form_resp.keys())
            self.assertNotEqual(len(corr_login_no_form_resp["professions"]), 0)
            self.assertNotEqual(len(corr_login_with_form_resp["professions"]), 0)
        with self.subTest(msg="assert response has courses inside"):
            self.assertTrue("courses" in corr_login_no_form_resp.keys())
            self.assertTrue("courses" in corr_login_with_form_resp.keys())
            self.assertNotEqual(len(corr_login_no_form_resp["courses"]), 0)
            self.assertNotEqual(len(corr_login_with_form_resp["courses"]), 0)
        with self.subTest(msg="assert correct return format"):
            self.assertEqual(
                list(corr_login_no_form_resp["courses"][0].keys()),
                ["name", "description"],
            )
            self.assertEqual(type(corr_login_no_form_resp["courses"][0]["name"]), str)
            self.assertEqual(
                type(corr_login_no_form_resp["courses"][0]["description"]), str
            )
            self.assertEqual(
                list(corr_login_with_form_resp["courses"][0].keys()),
                ["name", "description"],
            )
            self.assertEqual(type(corr_login_with_form_resp["courses"][0]["name"]), str)
            self.assertEqual(
                type(corr_login_with_form_resp["courses"][0]["description"]), str
            )
        pass
