import db.db_classes as db
from pydantic import BaseModel
class RegisterData (BaseModel):
    login: str
    password: str
    name: str

class RegisterResponse (BaseModel):
    status: str

conn = db.connect_db()
def register_user(reg_data: RegisterData):
    print(conn.url)
    login = reg_data.login
    print(login,type(login))
    passw = reg_data.password
    lst = conn.session.query(db.LoginDataTable).filter_by(login=login).all()
    if (len(lst)!=0):
        return RegisterResponse(status='LogEx') #login exist
    try:
        new_user = db.UsersTable(name=reg_data.name)
        conn.session.add(new_user)
        conn.session.commit()
        conn.session.add(db.LoginDataTable(login=login,password=passw,user_id=new_user.id))
        conn.session.commit()
        return RegisterResponse(status='OK')
    except:
        return RegisterResponse(status='ERR')
        
    
        