import pytest
import requests
from pydantic import BaseModel


class AccessTokenRequest(BaseModel):
    access_token: str


class User(BaseModel):
    id: int
    first_name: str
    last_name: str


def test_access_token_required():
    request = {
        "access_token": "test1_token"
    }
    AccessTokenRequest(**request)


def test_users_get_response():
    response = [
        {"id": 1532151, "first_name": "Ivan", "last_name": "Vasiliev"},
        {"id": 4841511, "first_name": "Vasiliy", "last_name": "Dmitriev"}
    ]
    users = [User(**user) for user in response]


def test_access_token_required():
    request = {}
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)


def test_access_token_format():
    request = {
        "access_token": "invalid_token_format"
    }
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)


def test_users_get_success():
    response = [
        {"id": 1532151, "first_name": "Ivan", "last_name": "Vasiliev"},
        {"id": 4841511, "first_name": "Vasiliy", "last_name": "Dmitriev"}
    ]
    users = [User(**user) for user in response]
    assert len(users) == 2
    assert users[0].id == 1532151
    assert users[0].first_name == "Ivan"
    assert users[0].last_name == "Vasiliev"


def test_users_get_no_users():
    response = []
    users = [User(**user) for user in response]
    assert len(users) == 0


def test_user_format():
    user = {
        "id": "invalid_id_format",
        "first_name": "Ivan",
        "last_name": "Vasiliev"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_user_name_format():
    user = {
        "id": 1532151,
        "first_name": "Dmitriy",
        "last_name": "Sergeev"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_user_lastname_format():
    user = {
        "id": 1414141,
        "first_name": "Sergey",
        "last_name": "Vladimirov"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_users_get_one_user():
    response = [{"id": 1532151, "first_name": "Ivan", "last_name": "Vasiliev"}]
    users = [User(**user) for user in response]
    assert len(users) == 1
    assert users[0].id == 1532151
    assert users[0].first_name == "Ivan"
    assert users[0].last_name == "Vasiliev"


def test_users_get_max_users():
    response = [{"id": i, "first_name": "User", "last_name": str(i)} for i in range(1000)
                ]
    users = [User(**user) for user in response]
    assert len(users) == 1000
    assert users[-1].id == 999
    assert users[-1].first_name == "User"
    assert users[-1].last_name == "999"


def test_users_get_invalid_response():
    response = [{"invalid_attr": "value"}]
    with pytest.raises(ValueError):
        users = [User(**user) for user in response]
