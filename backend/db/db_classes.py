from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

DB_PATH = 'db/profilium.db'

class BaseTable(DeclarativeBase): pass

class UsersTable(BaseTable):
    __tablename__ = 'UsersTable'
    id = Column (Integer, primary_key=True)
    name = Column(String)
    rel_to_login_data_table = relationship('LoginDataTable', back_populates='fk_to_users_table')

class LoginDataTable(BaseTable):
    __tablename__ = 'LoginDataTable'
    login = Column (String, primary_key=True, unique=True, nullable=False)
    password = Column(String)
    user_id = Column(Integer,ForeignKey('UsersTable.id')) #FK
    fk_to_users_table = relationship('UsersTable', back_populates='rel_to_login_data_table')

class CoursesTable(BaseTable):
    __tablename__ = 'CoursesTable'
    course_name = Column(String, primary_key=True, unique=True, nullable=False)
    description = Column(String)
    profession_id = Column(Integer,ForeignKey('ProfessionsTable.id')) #FK
    fk_to_professions_table = relationship('ProfessionsTable', back_populates='rel_to_courses_table')

class ProfessionsTable(BaseTable):
    __tablename__ = 'ProfessionsTable'
    id = Column(Integer,primary_key=True)
    name = Column(String,unique=True)
    description = Column(String)
    rel_to_courses_table = relationship('CoursesTable', back_populates='fk_to_professions_table')

class SingletonConnection (object):
    def __new__(cls,url):
        if not hasattr(cls,'instance'):
            cls.instance = super(SingletonConnection,cls).__new__(cls)
        return cls.instance

    def __init__(self, url) -> None:
        self.db_engine = create_engine(url)
        BaseTable.metadata.create_all(bind = self.db_engine)
        self._Session = sessionmaker(autoflush = True, bind = self.db_engine)
        self.session = self._Session(autoflush = True, bind = self.db_engine)

def connect_db(path = None):
    if(path == None):
        return SingletonConnection('sqlite:///'+DB_PATH)
    return SingletonConnection('sqlite:///'+path)

if __name__ == '__main__':
    db_connection = connect_db()
    tom = UsersTable(name='TOM')
    bob = UsersTable(name='BOB')
    db_connection.session.add(tom)
    db_connection.session.add(bob)
    db_connection.session.commit()
    print(tom.id)
    print(bob.id)
    users = db_connection.session.query(UsersTable).all()
    for i in users:
        print(i.id, i.name)