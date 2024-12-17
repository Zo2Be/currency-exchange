from httpx import Response
import pytest
from fastapi.testclient import TestClient
from app.api.endpoints.users import (
    get_user_from_db,
    is_password_good,
    get_database,
)
from currency_exchange.main import api_v1_app

client = TestClient(api_v1_app)


@pytest.fixture(name="passwords")
def fixture_passwords() -> dict[str, str]:
    passwords: dict = {
        "good_password": "@gOOd123@",
        "bad_password": "123",
    }
    return passwords


@pytest.fixture(name="user")
def fixture_user() -> dict[str, str]:
    user: dict = {
        "username": "kot",
        "true_password": "@gOOd123@",  # @gOOd123@
        "false_password": "dog",
    }
    return user


@pytest.fixture(name="usernames")
def fixture_usernames() -> dict[str, str]:
    usernames: dict[str, str] = {
        "exists_username": "root",
        "not_exists_username": "new_user",
    }
    return usernames


@pytest.fixture(name="database")
def fixture_database():
    database: list[dict[str, str]] = [
        {"username": "root", "password": "123"},
    ]
    return database


class TestGetUserFromDB:

    def test_is_user_exists_true(self, usernames) -> None:
        username = usernames["exists_username"]
        assert get_user_from_db(username)

    def test_is_user_exists_false(self, usernames) -> None:
        username = usernames["not_exists_username"]
        assert not get_user_from_db(username)


class TestIsPasswordGood:

    def test_is_password_good(self) -> None:
        password = "@gOOd123@"
        assert is_password_good(password)

    def test_is_password_bad(self) -> None:
        password = "123"
        assert not is_password_good(password)


class TestRegistration:

    def test_registration_with_not_user_and_bad_password(
        self, usernames, passwords
    ) -> None:
        username = usernames["not_exists_username"]
        password = passwords["bad_password"]

        login_data = {"username": username, "password": password}

        response: Response = client.post("/auth/register/", json=login_data)

        assert response.status_code == 200

        assert response.json() == {
            "message": "1. Has minimum 8 characters in length. "
            "2. At least one uppercase English letter. "
            "3. At least one lowercase English letter. "
            "4. At least one digit. "
            "5. At least one special character."
        }

    def test_registration_with_not_user_and_good_password(
        self, usernames, passwords
    ) -> None:

        username = usernames["not_exists_username"]
        password = passwords["good_password"]
        login_data = {"username": username, "password": password}

        response: Response = client.post("/auth/register/", json=login_data)

        assert response.status_code == 200

        assert response.json() == {"message": f"Welcome to the club, {username}"}

    def test_registration_with_user_and_good_password(
        self, usernames, passwords
    ) -> None:
        username = usernames["exists_username"]
        password = passwords["good_password"]

        login_data = {"username": username, "password": password}

        response: Response = client.post("/auth/register/", json=login_data)

        assert response.status_code == 200

        assert response.json() == {"error": "A user with this same name already exists"}

    def test_registration_with_user_and_bad_password(
        self, usernames, passwords
    ) -> None:
        username = usernames["exists_username"]
        password = passwords["bad_password"]

        login_data = {"username": username, "password": password}

        response: Response = client.post("/auth/register/", json=login_data)

        assert response.status_code == 200

        assert response.json() == {"error": "A user with this same name already exists"}


def test_add_user_after_registration(usernames, passwords):
    username = usernames["not_exists_username"]
    password = passwords["good_password"]

    login_data = {"username": username, "password": password}

    response: Response = client.post("/auth/register/", json=login_data)
    assert response.status_code == 200

    data = get_database()

    assert any(username == d["username"] for d in data)


class TestLogin:

    def test_login_with_user_exists(self, user) -> None:

        username = user["username"]
        password = user["true_password"]

        login_data = {
            "username": username,
            "password": password,
            "grant_type": "password",
        }

        headers = {"content-type": "application/x-www-form-urlencoded"}

        response: Response = client.post(
            "/auth/login/", data=login_data, headers=headers
        )
        response_data = response.json()

        assert response.status_code == 200
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"
        assert isinstance(response_data["access_token"], str)

    def test_login_with_user_not_exists(self, user) -> None:
        username = user["username"]
        password = user["false_password"]

        login_data = {
            "username": username,
            "password": password,
            "grant_type": "password",
        }

        headers = {"content-type": "application/x-www-form-urlencoded"}

        response: Response = client.post(
            "/auth/login/", data=login_data, headers=headers
        )

        assert response.status_code == 401
