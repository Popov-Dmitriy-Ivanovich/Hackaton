import db.db_classes as db
from pydantic import BaseModel
class LoginData (BaseModel):
    login: str
    password: str

class LoginResponce (BaseModel):
    status: str
conn = db.connect_db()
def process_login(log_data: LoginData):
    print(conn.url)
    login = log_data.login
    print(login,type(login))
    passw = log_data.password
    selection = conn.session.query(db.LoginDataTable).filter_by(login=login).first()
    print(selection,type(selection))
    if (selection and selection.password == passw):
        return LoginResponce(status='OK')
    return LoginResponce(status='ERR')