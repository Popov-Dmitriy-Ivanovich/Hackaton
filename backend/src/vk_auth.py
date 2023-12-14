from requests import request
from src.config import CLIENT_ID, CLIENT_SECRET
from db.db_classes import connect_db,UsersTable,LoginDataTable
class VkAuth (object):
    def __init__(self, code: str, state: str) -> None:
        self._code = code
        self._state= state
    
    def request_vk_access_token(self):
        auth_url = 'https://oauth.vk.com/access_token'
        auth_url += '?client_id='+CLIENT_ID
        auth_url += '&client_secret='+CLIENT_SECRET
        auth_url += '&redirect_uri=https://89.232.176.33:443/api/login_index'
        auth_url += '&code='+self.code
        r = request('get',auth_url)
        vk_responce = r.json()
        if ('error' in vk_responce.keys()):
            raise Exception('error while logining into VK')
        return vk_responce
    
    def add_user_vk_data_to_db(self):
        user_login = self._state
        conn = connect_db()
        login_entity = conn.session.query(LoginDataTable).filter_by(login=user_login).first()
        if (login_entity == None):
            raise Exception('user not found')
        user_entity = conn.session.query(UsersTable).filter_by(id=login_entity.user_id).first()
        if (user_entity == None):
            raise Exception('something wrong with database login exists, but user doesnt')
        vk_user_data = self.request_vk_access_token()
        user_entity.access_token=vk_user_data['access_token']
        user_entity.vk_id = vk_user_data['user_id']
        conn.session.commit()
        
        