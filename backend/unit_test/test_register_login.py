import requests as req
import unittest
import db.db_classes as db
from src.login import process_login

URL = "http://localhost:8000"


class TestAPI(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.conn = db.Connection("db/profilium.db")
        super().__init__(methodName)

    def test_login(self):
        correct_login_instance = self.conn.session.query(db.LoginDataTable).first()
        correct_login = {
            "login": correct_login_instance.login,
            "password": correct_login_instance.password,
        }
        incorrect_login = correct_login.copy()
        incorrect_login["password"] += "fjalj"

        with self.subTest(msg="test correct login"):
            resp = req.request("post", URL + "/api/login", json=correct_login)
            self.assertEqual(resp.json(), {"status": "OK"})

        with self.subTest(msg="test incorrect login"):
            resp = req.request("post", URL + "/api/login", json=incorrect_login)
            self.assertEqual(resp.json(), {"status": "ERR"})

    def test_register(self):
        correct_register = {
            "name": "TestRegister",
            "login": "TestRegister",
            "password": "TestRegister",
        }
        tmp = (
            self.conn.session.query(db.LoginDataTable)
            .filter_by(login=correct_register["login"])
            .first()
        )
        if tmp:
            tmp2 = (
                self.conn.session.query(db.UsersTable).filter_by(id=tmp.user_id).first()
            )
            self.conn.session.delete(tmp)
            self.conn.session.delete(tmp2)
            self.conn.session.commit()
        incorrect_register = {"name": "any name", "login": "TestRegister", "password": "1"}
        with self.subTest(msg="test correct register"):
            resp = req.request("post", URL + "/api/register", json=correct_register)
            self.assertEqual(resp.json(), {"status": "OK"})

        with self.subTest(msg="test incorrect register"):
            resp = req.request("post", URL + "/api/register", json=incorrect_register)
            self.assertEqual(resp.json(), {"status": "LogEx"})

        with self.subTest(msg="login after register"):
            resp = req.request(
                "post",
                URL + "/api/login",
                json={
                    "login": correct_register["login"],
                    "password": correct_register["password"],
                },
            )
            self.assertEqual(resp.json(), {"status": "OK"})
