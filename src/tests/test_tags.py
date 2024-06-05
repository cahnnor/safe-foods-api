import pytest
from app.helpers import DBHelpers as db


class TestUsers:

    @pytest.mark.parametrize("TagsResponse", ["GET"], indirect=True)
    def test_get(self, client, TagsResponse: dict):
        response: dict = client.get('/tags').json
        assert response == TagsResponse

    @pytest.mark.parametrize("TagsResponse", ["POST"], indirect=True)
    def test_post(self, client, TagsResponse: dict):
        response: dict = client.post(
            '/tags', json={"tag": "test", "dish_name": "Chicken Shawarma Wrap", "restaurant_name": "Shawarma Palace"}).json

        # Make sure tag exists.
        db_response: dict = db.get("SELECT tag FROM tags WHERE tag='test';")

        # Cleanup tag.
        db.commit("DELETE FROM tags WHERE tag='test';")
        assert response == TagsResponse
        assert len(db_response['data']) > 0

    @pytest.mark.parametrize("TagsResponse", ["DELETE"], indirect=True)
    def test_delete(self, client, TagsResponse: dict):
        # Create tag to be deleted:
        db.commit(
            "INSERT INTO tags (tag, dish_name, restaurant_name) VALUES ('test', 'Chicken Shawarma Wrap', 'Shawarma Palace');")

        response: dict = client.delete(
            '/tags/Shawarma%20Palace/Chicken%20Shawarma%20Wrap/test').json

        # Make sure tag was deleted.
        db_response: dict = db.get("SELECT tag FROM tags WHERE tag='test';")

        assert response == TagsResponse
        assert len(db_response['data']) == 0
