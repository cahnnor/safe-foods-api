import pytest
from app.helpers import DBHelpers as db


class TestRestaurants:

    @pytest.mark.parametrize("Restaurants", ["GET"], indirect=True)
    def test_get(self, client, Restaurants: dict):
        response: dict = client.get('/restaurants').json
        assert response == Restaurants

    @pytest.mark.parametrize("query, Restaurants", [({"restaurant_name": "test restaurant"}, "POST")], indirect=["Restaurants"])
    def test_post(self, client, query, Restaurants: dict):
        # Add to DB through POST request.
        response: dict = client.post('/restaurants', json=query).json

        # Make sure it was added.
        db_response: dict = db.get(
            "SELECT restaurant_name FROM restaurants WHERE restaurant_name='test restaurant';")

        # Clean up.
        db.commit(
            "DELETE FROM restaurants WHERE restaurant_name='test restaurant';")

        assert response == Restaurants
        assert len(db_response['data']) > 0

    @pytest.mark.parametrize("query, Restaurants", [({
        "proximity": 2.5,
        "delivery_time": 30.0,
        "restaurant_name": "test restaurant"
    }, "PUT")], indirect=["Restaurants"])
    def test_put(self, client, query, Restaurants: dict):
        # Add restaurant in advance:
        db.commit(
            "INSERT INTO restaurants (restaurant_name) VALUES ('test restaurant');")

        # Update restaurant info
        response: dict = client.put('/restaurants', json=query).json

        # Check info is correct.
        db_response: dict = db.get(
            "SELECT delivery_time, proximity, restaurant_name FROM restaurants WHERE restaurant_name='test restaurant';")

        # Clean up
        db.commit(
            "DELETE FROM restaurants WHERE restaurant_name='test restaurant';")
        print(db_response['data'])
        assert db_response['data'] == [
            {"proximity": 2.5, "delivery_time": 30.0, "restaurant_name": "test restaurant"}]
        assert response == Restaurants

    @pytest.mark.parametrize("query, Restaurants", [("test%20restaurant", "DELETE")], indirect=["Restaurants"])
    def test_delete(self, client, query, Restaurants: dict):
        # Add restaurant in advance:
        db.commit(
            "INSERT INTO restaurants (restaurant_name) VALUES ('test restaurant');")

        # Delete it.
        response: dict = client.delete(
            f'/restaurants/{query}', json=query).json

        # Make sure it's gone:
        db_response: dict = db.get(
            "SELECT * FROM restaurants WHERE restaurant_name='test restaurant';")

        assert response == Restaurants
        assert len(db_response['data']) == 0
