import unittest
from unit_test.testing_supplies import DbOperations, Expectation
from requests import request

URL = "http://localhost:8000/api/login"

expect_422 = Expectation(422, lambda x, y: x == y.status_code)
expect_ok = Expectation({"status": "OK"}, lambda x, y: x == y.json())
expect_err = Expectation({"status": "ERR"}, lambda x, y: x == y.json())

db_handler = DbOperations()


class TestApiLogin(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self._test_data = [
            ["TestLogin1", "TestPassword1", expect_ok],
            ["TestLogin1", None, expect_422],
            ["TestLogin1", "WrongPassword", expect_err],
            ["TestLogin1", "", expect_err],
            ["WrongLogin", "WrongPassword", expect_err],
            ["WrongLogin", "", expect_err],
            ["WrongLogin", "TestPassword1", expect_err],
            ["WrongLogin", None, expect_422],
            [None, "WrongPassword", expect_422],
            [None, "", expect_422],
            [None, None, expect_422],
            [None, "TestPassword1", expect_422],
            ["", "", expect_err],
            ["", None, expect_422],
            ["", "WrongPassword", expect_err],
            ["", "TestPassword1", expect_err],
        ]
        super().__init__(methodName)

    def test_different_logins(self):
        for log_data in self._test_data:
            with self.subTest(msg=f"testing{log_data}"):
                body = {"login": log_data[0], "password": log_data[1]}
                if log_data[0] == None:
                    body = {"password": log_data[1]}
                if log_data[1] == None:
                    body = {"login": log_data[0]}
                if log_data[0] == None and log_data[1] == None:
                    body = {}
                self.assertTrue(
                    log_data[2].check_ex(request("post", URL, json=body)),
                    msg=f"{log_data}",
                )
                if log_data[2] == expect_ok:
                    self.assertNotEqual(
                        db_handler.get_login_entity(log_data[0]),
                        None,
                        msg=f"{log_data}, logged in but db has no login entity",
                    )
                    self.assertEqual(
                        db_handler.get_login_entity(log_data[0]).login,
                        log_data[0],
                        msg=f"{log_data} login with wrong login",
                    )
                    self.assertEqual(
                        db_handler.get_login_entity(log_data[0]).password,
                        log_data[1],
                        msg=f"{log_data} login with wrong password",
                    )
