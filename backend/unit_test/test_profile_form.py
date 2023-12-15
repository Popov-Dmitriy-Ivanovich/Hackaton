import unittest
from unit_test.testing_supplies import DbOperations, Expectation
from requests import request

URL = 'http://localhost:8000/api/profile_form_res'

expect_422 = Expectation(422,lambda x,y:x==y.status_code)
expect_ok = Expectation({'status':'OK'},lambda x,y: x==y.json())
expect_err = Expectation({'status':'ERR'},lambda x,y: x==y.json())

db_handler = DbOperations()

class TestProcessForm(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self._test_data = [
            [None,['str'],expect_422],
            [None,[],expect_422],
            [None,[None],expect_422],
            ['TestLogin1',[None],expect_422],
            ['TestLogin1',[1,2,3],expect_422],
            ['TestLogin1','str',expect_422],
            ['IncorrectTestFormLogin',['str'],expect_err],
            ['IncorrectTestFormLogin',['str','str','str'],expect_err],
            ['IncorrectTestFormLogin',[],expect_err],
            ['TestLogin1',['str'],expect_ok],
            ['TestLogin1',['str','str','str'],expect_ok],
            ['TestLogin1',[],expect_ok]
        ]
        super().__init__(methodName)
    def test_different_logins(self):
        for log_data in self._test_data:
            with self.subTest(msg=f'testing{log_data}'):
                body = {'login':log_data[0],'choises':log_data[1]}
                if log_data[0]==None:
                    body = {'choises':log_data[1]}
                if log_data[1]==None:
                    body = {'login':log_data[0]}
                if log_data[0]==None and log_data[1]==None:
                    body = {}
                self.assertTrue(log_data[2].check_ex(request('post',URL,json=body)))
                if log_data[2]==expect_ok:
                    log_entity = db_handler.get_login_entity(log_data[0])
                    favourites = db_handler.get_favourites(log_entity.user_id)
                    self.assertEqual(len(favourites),len(log_data[1]))
                    for i in favourites:
                        self.assertTrue(i.name in log_data[1])