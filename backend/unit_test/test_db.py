from db.db_classes import UsersTable, LoginDataTable, CoursesTable, ProfessionsTable, SingletonConnection, connect_db,Connection
import unittest


class TestDbConnection(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        print('db_init')
        self.db_connection = Connection('unit_test/resourses/test.db')
        self._clear_db()
        super().__init__(methodName)

    def _clear_db(self):
        users = self.db_connection.session.query(UsersTable).all()
        login = self.db_connection.session.query(LoginDataTable).all()
        cours = self.db_connection.session.query(CoursesTable).all()
        proff = self.db_connection.session.query(ProfessionsTable).all()
        for row in users:
            self.db_connection.session.delete(row)
        for row in login:
            self.db_connection.session.delete(row)
        for row in cours:
            self.db_connection.session.delete(row)
        for row in proff:
            self.db_connection.session.delete(row)
        self.db_connection.session.commit()
    
    def test_users_table(self):
        rows = []

        with self.subTest(msg='testing insertion'):
            u1 = UsersTable(name='TestUser1')
            u2 = UsersTable(name='TestUser2')
            self.db_connection.session.add(u1)
            self.db_connection.session.add(u2)
            self.db_connection.session.commit()
            rows.append(u1)
            rows.append(u2)

        with self.subTest(msg = 'testing updating'):
            to_update = self.db_connection.session.query(UsersTable).filter_by(id = rows[0].id)
            to_update.name='RenamedUser1'
            self.db_connection.session.commit()
            rows[0].name='RenamedUser1'

        with self.subTest(msg='testing deleting'):
            del_id = self.db_connection.session.query(UsersTable).filter_by(id = rows[1].id).first()
            self.db_connection.session.delete(del_id)
            self.db_connection.session.commit()
            rows = rows[:-1]

        with self.subTest(msg='testing selecting'):
            selection = self.db_connection.session.query(UsersTable).all()
            self.assertEqual(len(selection),len(rows))
            for i in range(len(rows)):
                self.assertEqual(selection[i],rows[i])

    def test_professions_talbe(self):
        rows = []
        with self.subTest(msg='testing insertion'):
            u1 = ProfessionsTable(name='Prof1')
            u2 = ProfessionsTable(name='Prof2')
            self.db_connection.session.add(u1)
            self.db_connection.session.add(u2)
            self.db_connection.session.commit()
            rows.append(u1)
            rows.append(u2)

        with self.subTest(msg = 'testing updating'):
            to_update = self.db_connection.session.query(ProfessionsTable).filter_by(id = rows[0].id).first()
            to_update.name='RenamedProf1'
            self.db_connection.session.commit()
            rows[0].name='RenamedProf1'

        with self.subTest(msg='testing deleting'):
            del_id = self.db_connection.session.query(ProfessionsTable).filter_by(id = rows[1].id).first()
            self.db_connection.session.delete(del_id)
            self.db_connection.session.commit()
            rows = rows[:-1]

        with self.subTest(msg='testing selecting'):
            selection = self.db_connection.session.query(ProfessionsTable).all()
            self.assertEqual(len(selection),len(rows))
            for i in range(len(rows)):
                self.assertEqual(selection[i],rows[i])

    def test_login_data_table(self):
        rows = []
        with self.subTest(msg='testing insertion'):
            u1 = LoginDataTable(login='Prof1', password='123')
            u2 = LoginDataTable(login='Prof2', password='321')
            self.db_connection.session.add(u1)
            self.db_connection.session.add(u2)
            self.db_connection.session.commit()
            rows.append(u1)
            rows.append(u2)
        with self.subTest(msg = 'testing updating'):
            to_update = self.db_connection.session.query(LoginDataTable).filter_by(login = rows[0].login).first()
            to_update.login='login1'
            self.db_connection.session.commit()
            rows[0].login='login1'
        with self.subTest(msg='testing deleting'):
            del_id = self.db_connection.session.query(LoginDataTable).filter_by(login = rows[1].login).first()
            self.db_connection.session.delete(del_id)
            self.db_connection.session.commit()
            rows = rows[:-1]
        with self.subTest(msg='testing selecting'):
            selection = self.db_connection.session.query(LoginDataTable).all()
            self.assertEqual(len(selection),len(rows))
            for i in range(len(rows)):
                self.assertEqual(selection[i],rows[i])

    def test_courses_table(self):
        rows = []
        with self.subTest(msg='testing insertion'):
            u1 = CoursesTable(course_name='Prof1',profession_id=1)
            u2 = CoursesTable(course_name='Prof2',profession_id=1)
            self.db_connection.session.add(u1)
            self.db_connection.session.add(u2)
            self.db_connection.session.commit()
            rows.append(u1)
            rows.append(u2)

        with self.subTest(msg = 'testing updating'):
            to_update = self.db_connection.session.query(CoursesTable).filter_by(course_name = rows[0].course_name).first()
            to_update.course_name='RenamedProf1'
            self.db_connection.session.commit()
            rows[0].course_name='RenamedProf1'

        with self.subTest(msg='testing deleting'):
            del_id = self.db_connection.session.query(CoursesTable).filter_by(course_name = rows[1].course_name).first()
            self.db_connection.session.delete(del_id)
            self.db_connection.session.commit()
            rows = rows[:-1]

        with self.subTest(msg='testing selecting'):
            selection = self.db_connection.session.query(CoursesTable).all()
            self.assertEqual(len(selection),len(rows))
            for i in range(len(rows)):
                self.assertEqual(selection[i],rows[i])
    
if __name__ == '__main__':
    print('test should be executed from run_test.py')