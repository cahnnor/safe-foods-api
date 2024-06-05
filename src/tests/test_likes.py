import pytest
from app.helpers import DBHelpers as db


class TestLikes:

    @pytest.mark.parametrize("req, LikesResponse",
                             [("?dish_name=Chicken%20Shawarma%20Platter&restaurant_name=Ozzy's",
                              "?dish_name=Chicken%20Shawarma%20Platter&restaurant_name=Ozzy's")], indirect=["LikesResponse"])
    def test_get(self, client, req, LikesResponse: dict):
        response: dict = client.get('/likes' + req).json
        assert response == LikesResponse

    @pytest.mark.parametrize("req, LikesResponse",
                             [({"user_name": "Connor", "dish_name": "Chicken Shawarma Wrap", "restaurant_name": "Shawarma Palace"},
                               "POST")], indirect=["LikesResponse"])
    def test_post(self, client, req, LikesResponse: dict):
        response: dict = client.post('/likes', json=req).json

        # Make sure like exists.
        db_response: dict = db.get(
            "SELECT * FROM likes WHERE user_name='Connor' AND dish_name='Chicken Shawarma Wrap' AND restaurant_name='Shawarma Palace';")

        # Cleanup like.
        db.commit("DELETE FROM likes WHERE user_name='Connor' AND dish_name='Chicken Shawarma Wrap' AND restaurant_name='Shawarma Palace';")
        assert response == LikesResponse
        assert len(db_response['data']) > 0

    @pytest.mark.parametrize("req, LikesResponse",
                             [("Shawarma%20Palace/Chicken%20Shawarma%20Wrap/Connor",
                               "DELETE")], indirect=["LikesResponse"])
    def test_delete(self, client, req, LikesResponse: dict):
        # Create like to be deleted:
        db.commit("INSERT INTO likes (user_name, dish_name, restaurant_name) VALUES ('Connor', 'Chicken Shawarma Wrap', 'Shawarma Palace');")

        response: dict = client.delete(f'/likes/{req}').json

        # Make sure like was deleted.
        db_response: dict = db.get(
            "SELECT * FROM likes WHERE user_name='Connor' AND dish_name='Chicken Shawarma Wrap' AND restaurant_name='Shawarma Palace';")

        assert response == LikesResponse
        assert len(db_response['data']) == 0
