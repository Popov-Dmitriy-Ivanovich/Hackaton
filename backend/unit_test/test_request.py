import requests as req
import unittest
import db.db_classes as db
from src.login import process_login

URL = 'http://localhost:8000'

class TestAPI(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.conn = db.Connection('db/profilium.db')
        self._clear_db()
        self.conn.session.add(db.UsersTable(name='TestUser1'))
        self.conn.session.add(db.LoginDataTable(login='1',password='1',user_id=1))
        self.conn.session.commit()
        super().__init__(methodName)


    def _clear_db(self):
        users = self.conn.session.query(db.UsersTable).all()
        login = self.conn.session.query(db.LoginDataTable).all()
        cours = self.conn.session.query(db.CoursesTable).all()
        proff = self.conn.session.query(db.ProfessionsTable).all()
        for row in users:
            self.conn.session.delete(row)
        for row in login:
            self.conn.session.delete(row)
        for row in cours:
            self.conn.session.delete(row)
        for row in proff:
            self.conn.session.delete(row)
        self.conn.session.commit()

    def test_login(self):
        pass
        correct_login_instance = self.conn.session.query(db.LoginDataTable).first()
        correct_login = {'login':correct_login_instance.login,'password':correct_login_instance.password}
        incorrect_login = correct_login.copy()
        incorrect_login['password']+='fjalj'

        with self.subTest(msg = 'test correct login'):
            resp = req.request('post',URL+'/api/login',json=correct_login)
            self.assertEqual(resp.json(),{'status': 'OK'})

        with self.subTest(msg = 'test incorrect login'):
            resp = req.request('post',URL+'/api/login',json=incorrect_login)
            self.assertEqual(resp.json(),{'status': 'ERR'})

    def test_register(self):
        correct_register = {'name':'dmitriy','login':'popov','password':'ivanovich'}
        incorrect_register = {'name':'any name',"login":'1','password':'1'}
        with self.subTest(msg='test correct register'):
            resp = req.request('post',URL+'/api/register',json=correct_register)
            self.assertEqual(resp.json(),{'status': 'OK'})
        
        with self.subTest(msg='test incorrect register'):
            resp = req.request('post',URL+'/api/register',json=incorrect_register)
            self.assertEqual(resp.json(),{'status': 'LogEx'})

        with self.subTest(msg='login after register'):
            resp = req.request('post',URL+'/api/login',json={'login':'popov','password':'ivanovich'})
            self.assertEqual(resp.json(),{'status': 'OK'})



#if __name__ == '__main__':
#    print ('server should be online to perform that test!!!')
#    r = req.request("post", "http://localhost:8000/api/login",json={'login':'1','password':'1'})
#    print(r.text)
#    r = req.request("post", "http://localhost:8000/api/login",json={'login':'3','password':'3'})
#    print(r.text)
#    r = req.request("post", "http://localhost:8000/api/get_courses")
#    print(r.text)
