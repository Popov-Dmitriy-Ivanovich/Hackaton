import vk

class VkApiResolver(object):
    def __init__(self,token,id_user) -> None:
        self._token = token
        self._id_user = id_user
        self._vk_api = vk.API(self._token)
    
    def get_user_subscriptions(self):
        response = self._vk_api.users.getSubscriptions(user_id=self._id_user, v=5.92)
        return response["groups"]["items"][:15]
    
    def get_group_info(self,group_id):
        response = self._vk_api.groups.getById(group_id=group_id, fields="description", v=5.92)
        return response[0]["name"], response[0]["description"]