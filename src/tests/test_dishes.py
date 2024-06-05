import pytest
from app.helpers import DBHelpers as db


class TestDishes:
    """
    Compares a collection of queries against the test client to fixtures.
    Tests pulling dishes with and without a number of tags.
    """
    @pytest.mark.parametrize("query, DishesResponse", [("", ""),
                                                       ("?user=Connor",
                                                        "?user=Connor"),
                                                       ("?user=Connor&user=Not%20Connor",
                                                        "?user=Connor&user=Not%20Connor"),
                                                       ("?tag=Halal",
                                                        "?tag=Halal"),
                                                       ("?tag=Halal&tag=Lactose-Free",
                                                        "?tag=Halal&tag=Lactose-Free"),
                                                       ("?user=Not%20Connor&tag=Lactose-Free", "?user=Not%20Connor&tag=Lactose-Free")],
                             indirect=["DishesResponse"])
    def test_get(self, client, query, DishesResponse: dict):
        response: dict = client.get('/dishes' + query).json
        assert response == DishesResponse

    def test_post(self, client, DishesPost: dict):
        response: dict = client.post(
            '/dishes', json={"dish_name": "test dish", "restaurant_name": "Shawarma Palace"}).json

        db_response: dict = db.get(
            "SELECT dish_name FROM dishes WHERE dish_name='test dish';")
        db.commit("DELETE FROM dishes WHERE dish_name='test dish';")
        assert response == DishesPost
        assert len(db_response) > 0

    def test_delete(self, client, DishesDelete: dict):
        db.commit(
            "INSERT INTO dishes (dish_name, restaurant_name) VALUES ('test dish', 'Shawarma Palace');")
        response: dict = client.delete(
            '/restaurants/Shawarma%20Palace/test%20dish').json

        db_response: dict = db.get(
            "SELECT dish_name FROM dishes WHERE dish_name='test dish';")
        assert response == DishesDelete
        assert len(db_response['data']) == 0
