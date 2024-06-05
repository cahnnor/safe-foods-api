import pytest
from app.helpers import DBHelpers as db


class TestUsers:

    @pytest.mark.parametrize("UsersResponse", ["GET"], indirect=True)
    def test_get(self, client, UsersResponse: dict):
        response: dict = client.get('/users').json
        assert response == UsersResponse

    @pytest.mark.parametrize("UsersResponse", ["POST"], indirect=True)
    def test_post(self, client, UsersResponse: dict):
        response: dict = client.post(
            '/users', json={"user_name": "Test User"}).json

        # Make sure user exists.
        db_response: dict = db.get(
            "SELECT user_name FROM users WHERE user_name='Test User';")

        # Cleanup user.
        db.commit("DELETE FROM users WHERE user_name='Test User';")
        assert response == UsersResponse
        assert len(db_response['data']) > 0

    @pytest.mark.parametrize("UsersResponse", ["DELETE"], indirect=True)
    def test_delete(self, client, UsersResponse: dict):
        # Create user to be deleted:
        db.commit("INSERT INTO users (user_name) VALUES ('Test User');")

        response: dict = client.delete(
            '/users/Test%20User').json

        # Make sure user was deleted.
        db_response: dict = db.get(
            "SELECT user_name FROM users WHERE user_name='Test User';")

        assert response == UsersResponse
        assert len(db_response['data']) == 0
