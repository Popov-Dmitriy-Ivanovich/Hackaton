from db.db_classes import connect_db, UsersTable, LoginDataTable, FavouritesTable
class DbOperations (object):
    def __init__(self) -> None:
        self._conn = connect_db()

    def get_users(self):
        return self._conn.session.query(UsersTable).all()
    
    def get_logins(self):
        return self._conn.session.query(LoginDataTable).all()
    
    def get_favourites(self,user_id):
        return self._conn.session.query(FavouritesTable).filter_by(user_id=user_id).all()
    
    def get_user(self, user_id):
        return self._conn.session.query(UsersTable).filter_by(id = user_id).first()
    
    def get_login(self,user_id):
        return self._conn.session.query(LoginDataTable).filter_by(user_id = user_id).first()
    
    def get_login_entity(self,login):
        return self._conn.session.query(LoginDataTable).filter_by(login = login).first()
    
class Expectation():
    def __init__(self, expect,comp_function = None) -> None:
        self.expect = expect
        if comp_function != None:
            self.comp_function=comp_function
        else:
            self.comp_function=lambda x,y: x==y
    def check_ex(self,value):
        return self.comp_function(self.expect, value)