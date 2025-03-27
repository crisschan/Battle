import pytest
import allure
import json

@allure.epic('Battle Game API Tests')
class TestBattleAPI:

    @allure.feature('Index Page')
    def test_index(self, session, base_url):
        response = session.get(f'{base_url}/index')
        data = response.json()
        
        assert response.status_code == 200
        assert data['code'] == 0
        assert data['message'] == 'Success'
        assert 'instruction' in data['data']

    @allure.feature('Login')
    @pytest.mark.parametrize('credentials,expected', [
        ({'username': 'test', 'password': 'test'}, {'code': 0, 'message': 'Success'}),
        ({'username': 'wrong', 'password': 'wrong'}, {'code': 9901, 'message': 'Username or Password Error'}),
        ({'username': 'testuser'}, {'code': 9906, 'message': 'Invalid JSON Input'}),
    ])
    def test_login(self, session, base_url, credentials, expected):
        response = session.post(f'{base_url}/login', json=credentials)
        data = response.json()

        assert response.status_code == 200
        assert data['code'] == expected['code']
        assert data['message'] == expected['message']
        if data['code'] == 0:
            assert 'equipment_options' in data['data']

    @allure.feature('Equipment Selection')
    @pytest.mark.parametrize('equipment_id,expected', [
        ('10001', {'code': 0, 'message': 'Success'}),
        ('10002', {'code': 0, 'message': 'Success'}),
        ('10003', {'code': 0, 'message': 'Success'}),
        ('invalid', {'code': 9902, 'message': 'Invalid Equipment Selection'}),
        (None, {'code': 9902, 'message': 'Invalid Equipment Selection'}),
    ])
    def test_select_equipment(self, logged_in_session, base_url, equipment_id, expected):
        response = logged_in_session.post(
            f'{base_url}/select',
            json={'equipmentid': equipment_id}
        )
        data = response.json()

        assert response.status_code == 200
        assert data['code'] == expected['code']
        assert data['message'] == expected['message']
        if data['code'] == 0:
            assert 'enemy_options' in data['data']
            assert data['data']['equipmentid'] == equipment_id

    @allure.feature('Battle System')
    @pytest.mark.parametrize('equipment_id,enemy_id,expected', [
        ('10001', '20001', {'code': 0, 'message': 'Success'}),
        ('10002', '20002', {'code': 0, 'message': 'Success'}),
        ('10003', '20003', {'code': 0, 'message': 'Success'}),
        ('10001', 'invalid', {'code': 9902, 'message': 'Invalid Enemy ID'}),
        ('invalid', '20001', {'code': 9903, 'message': 'Invalid Equipment ID'}),
        (None, '20001', {'code': 9905, 'message': 'Equipment ID is required'}),
        ('10001', None, {'code': 9904, 'message': 'Enemy ID is required'}),
    ])
    def test_battle(self, logged_in_session, base_url, equipment_id, enemy_id, expected):
        response = logged_in_session.post(
            f'{base_url}/kill',
            json={
                'equipmentid': equipment_id,
                'enemyid': enemy_id
            }
        )
        data = response.json()

        assert response.status_code == 200
        assert data['code'] == expected['code']
        assert data['message'] == expected['message']
        
        if data['code'] == 0:
            assert 'status' in data['data']
            if data['data']['status'] == 'win':
                assert data['data']['level'] == 1
            elif data['data']['status'] == 'draw':
                assert data['data']['message'] == 'Both dead'
            elif data['data']['status'] == 'lose':
                assert data['data']['message'] == 'You died'