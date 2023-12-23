import requests

from app.settings import settings
from app.models.user import User


class IdentityRepo:
    def get_token_by_code(self, code: str) -> str:
        token_req_data = {
            'code': code,
            'client_id': settings.oauth2_client_id,
            'client_secret': settings.oauth2_client_secret,
            'grant_type': 'authorization_code'
        }
        token_data = requests.post(
            settings.oauth2_access_token_url, data=token_req_data).json()
        return token_data['access_token']

    def get_student_group(self, token: str) -> str:
        student_info = requests.get(settings.oauth2_student_details_url, headers={ 'Authorization': f'Bearer {token}' }).json()
        return student_info['group_name']

    def get_employee_unit(self, token: str) -> str:
        employee_info = requests.get(settings.oauth2_employee_details_url, headers={ 'Authorization': f'Bearer {token}' }).json()
        return employee_info['group_name']

    def get_user(self, token: str) -> User:
        userinfo = requests.get(settings.oauth2_user_details_url, headers={ 'Authorization': f'Bearer {token}' }).json()
        is_student = userinfo['username'].find('edu.mirea.ru') != -1
        return User(
            id=userinfo['uid'],
            name=f'{userinfo["lastname"]} {userinfo["name"]} {userinfo["middlename"]}',
            email=userinfo['email'],
            unit=self.get_student_group(token) if is_student else self.get_employee_unit(token)
        )
