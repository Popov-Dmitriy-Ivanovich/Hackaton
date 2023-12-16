import unittest
from unit_test.testing_supplies import DbOperations, Expectation
from requests import request

URL = "http://localhost:8000/api/register"
db_handler = DbOperations()

expect_422 = Expectation(422, lambda x, y: x == y.status_code)
expect_ok = Expectation({"status": "OK"}, lambda x, y: x == y.json())
expect_loginc = Expectation({"status": "LogInc"}, lambda x, y: x == y.json())
expect_passwinc = Expectation({"status": "PasswInc"}, lambda x, y: x == y.json())
expect_logex = Expectation({"status": "LogEx"}, lambda x, y: x == y.json())

incorrect_logins = [
    "",
    "@#)()",
    "afd@fdas_@123@",
    "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789",
    "@_213",
]
incorrect_passwords = incorrect_logins.copy()


class TestRegister(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.test_data = []

        # add 422 requests
        self.test_data.append([None, "RegisterLogin", "RegisterPassw", expect_422])
        for log in incorrect_logins:
            self.test_data.append([None, log, "RegisterPassw", expect_422])
        for pas in incorrect_passwords:
            self.test_data.append([None, "RegisterLogin", pas, expect_422])

        for log in incorrect_logins:
            self.test_data.append(["name", log, None, expect_422])
        for pas in incorrect_passwords:
            self.test_data.append(["None", None, pas, expect_422])

        # add all possible incorrect login requests
        for log in incorrect_logins:
            self.test_data.append(["Name", log, "RegisterPassw", expect_loginc])
            for pas in incorrect_passwords:
                self.test_data.append(["name", log, pas, expect_loginc])

        # add all possible incorrect password requests
        for pas in incorrect_passwords:
            self.test_data.append(["Name", "RegisterLogin", pas, expect_passwinc])

        # add correct register requests
        self.test_data.append(["name", "RegisterTestUser1", "passw", expect_ok])
        self.test_data.append(["", "RegisterTestUser2", "passw", expect_ok])

        # add existing login request
        self.test_data.append(["", "RegisterTestUser1", "passw", expect_logex])
        super().__init__(methodName)

    def test_registration(self):
        for log_data in self.test_data:
            with self.subTest(msg=f"testing{log_data}"):
                body = {
                    "name": log_data[0],
                    "login": log_data[1],
                    "password": log_data[2],
                }
                if log_data[0] == None:
                    body = {"login": log_data[1], "password": log_data[2]}
                if log_data[1] == None:
                    body = {"name": log_data[0], "password": log_data[2]}
                if log_data[2] == None:
                    body = {"name": log_data[0], "login": log_data[1]}
                if log_data[0] == None and log_data[1] == None:
                    body = {"password": log_data[2]}
                if log_data[0] == None and log_data[2] == None:
                    body = {"login": log_data[1]}
                if log_data[1] == None and log_data[2] == None:
                    body = {"name": log_data[0]}
                if log_data[0] == None and log_data[1] == None and log_data[2] == None:
                    body = {}
                self.assertTrue(
                    log_data[3].check_ex(request("post", URL, json=body)),
                    msg=request("post", URL, json=body).text,
                )
                if log_data[3] == expect_ok:
                    self.assertNotEqual(db_handler.get_login_entity(log_data[1]), None)
                    self.assertEqual(
                        db_handler.get_login_entity(log_data[1]).login, log_data[1]
                    )
                    self.assertEqual(
                        db_handler.get_login_entity(log_data[1]).password, log_data[2]
                    )
                elif log_data[3] != expect_422 and log_data[3] != expect_logex:
                    self.assertEqual(
                        db_handler.get_login_entity(log_data[1]), None, msg=log_data
                    )
