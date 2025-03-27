import pytest
import requests
from SQLiteHelper import SQLiteHelper

@pytest.fixture(scope='session')
def base_url():
    return 'http://localhost:12356'

@pytest.fixture(scope='session')
def db_helper():
    helper = SQLiteHelper('bat.db')
    yield helper
    helper.close()

@pytest.fixture(scope='function')
def session():
    """创建一个新的会话用于测试"""
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture(scope='function')
def logged_in_session(session, base_url):
    """创建一个已登录的会话用于测试"""
    login_data = {
        'username': 'testuser',
        'password': 'testuser'
    }
    session.post(f'{base_url}/login', json=login_data)
    return session