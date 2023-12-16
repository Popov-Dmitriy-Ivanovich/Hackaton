import db.db_classes as db
from pydantic import BaseModel


class RegisterData(BaseModel):
    login: str
    password: str
    name: str


class RegisterResponse(BaseModel):
    status: str


class UserCreator(object):
    def __init__(self) -> None:
        self._conn = db.connect_db()
        self._allowed_non_letter = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "0",
            "_",
        ]

    def _check_login(self, login: str):
        if login == "" or login == None or len(login) > 100:
            return False
        testing_login = login.replace("_", "")
        for let in self._allowed_non_letter:
            testing_login = testing_login.replace(let, "")
        return testing_login == "" or testing_login.isalpha()

    def _check_password(self, passwd: str):
        if passwd == "" or passwd == None or len(passwd) > 100:
            return False
        test_passw = passwd.replace("_", "")
        for let in self._allowed_non_letter:
            test_passw = test_passw.replace(let, "")
        return test_passw == "" or test_passw.isalpha()

    def _check_sql(self, inp_str: str):
        return True

    def register_user(self, reg_data: RegisterData):
        login = reg_data.login
        passw = reg_data.password
        if not self._check_login(login):
            return RegisterResponse(status="LogInc")  # login incorrect
        if not self._check_password(passw):
            return RegisterResponse(status="PasswInc")  # password incorrect
        if not self._check_sql(login):
            return RegisterResponse(status="SQL")
        if not self._check_sql(passw):
            return RegisterResponse(status="SQL")
        lst = self._conn.session.query(db.LoginDataTable).filter_by(login=login).all()
        if len(lst) != 0:
            return RegisterResponse(status="LogEx")
        try:
            new_user = db.UsersTable(name=reg_data.name)
            self._conn.session.add(new_user)
            self._conn.session.commit()
            self._conn.session.add(
                db.LoginDataTable(login=login, password=passw, user_id=new_user.id)
            )
            self._conn.session.commit()
            return RegisterResponse(status="OK")
        except:
            return RegisterResponse(status="ERR")


def register_user(reg_data: RegisterData):
    handler = UserCreator()
    return handler.register_user(reg_data)
