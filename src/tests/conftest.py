import pytest
from app import create_app

# This file holds fixtures for all of the Python Unit tests.


@pytest.fixture(scope="session")
def request_context():
    """
    Sets up app for testing requests, otherwise checking for request.method will error out since there is no real HTTP request.
    """
    app = create_app()
    return app.test_request_context


@pytest.fixture(scope="session")
def client():
    """
    Setup client for testing purposes.
    """
    app = create_app()

    c = app.test_client()
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def Restaurants(request) -> dict:
    if (request.param == "GET"):
        return {
            "data": [
                {
                    "delivery_time": 15.0,
                    "id": 1,
                    "proximity": 1.5,
                    "restaurant_name": "Shawarma Palace"
                },
                {
                    "delivery_time": 0.0,
                    "id": 2,
                    "proximity": 0.0,
                    "restaurant_name": "Ozzy's"
                }
            ],
            "status": 200
        }
    elif (request.param == "POST" or request.param == "PUT"):
        return {
            "data": "Commit successful!",
            "status": 200
        }
    elif (request.param == "DELETE"):
        return {
            "data": "Delete successful!",
            "status": 200
        }
    else:
        return {"data": "Bad use of fixture!", "status": 400}


@pytest.fixture(scope="session")
def DishesResponse(request) -> dict:
    if (request.param == ""):
        return {
            "data": {
                "Ozzy's": {
                    "dishes": {
                        "Chicken Shawarma Platter": {
                            "likes": [
                                "Connor"
                            ],
                            "tags": [
                                "Halal",
                                "Lactose-Free"
                            ]
                        }
                    }
                },
                "Shawarma Palace": {
                    "dishes": {
                        "Chicken Shawarma Wrap": {
                            "likes": [
                                "Not Connor"
                            ],
                            "tags": [
                                "Halal"
                            ]
                        }
                    }
                }
            },
            "status": 200
        }
    elif (request.param == "?user=Connor"):
        return {
            "data": {
                "Ozzy's": {
                    "dishes": {
                        "Chicken Shawarma Platter": {
                            "likes": [
                                "Connor"
                            ],
                            "tags": [
                                "Halal",
                                "Lactose-Free"
                            ]
                        }
                    }
                }
            },
            "status": 200
        }
    elif (request.param == "?user=Connor&user=Not%20Connor"):
        return {
            "data": {
                "Ozzy's": {
                    "dishes": {
                        "Chicken Shawarma Platter": {
                            "likes": [
                                "Connor"
                            ],
                            "tags": [
                                "Halal",
                                "Lactose-Free"
                            ]
                        }
                    }
                },
                "Shawarma Palace": {
                    "dishes": {
                        "Chicken Shawarma Wrap": {
                            "likes": [
                                "Not Connor"
                            ],
                            "tags": [
                                "Halal"
                            ]
                        }
                    }
                }
            },
            "status": 200
        }
    elif (request.param == "?tag=Halal"):
        return {
            "data": {
                "Ozzy's": {
                    "dishes": {
                        "Chicken Shawarma Platter": {
                            "likes": [
                                "Connor"
                            ],
                            "tags": [
                                "Halal"
                            ]
                        }
                    }
                },
                "Shawarma Palace": {
                    "dishes": {
                        "Chicken Shawarma Wrap": {
                            "likes": [
                                "Not Connor"
                            ],
                            "tags": [
                                "Halal"
                            ]
                        }
                    }
                }
            },
            "status": 200
        }
    elif (request.param == "?tag=Halal&tag=Lactose-Free"):
        return {
            "data": {
                "Ozzy's": {
                    "dishes": {
                        "Chicken Shawarma Platter": {
                            "likes": [
                                "Connor"
                            ],
                            "tags": [
                                "Halal",
                                "Lactose-Free"
                            ]
                        }
                    }
                },
                "Shawarma Palace": {
                    "dishes": {
                        "Chicken Shawarma Wrap": {
                            "likes": [
                                "Not Connor"
                            ],
                            "tags": [
                                "Halal"
                            ]
                        }
                    }
                }
            },
            "status": 200
        }
    elif (request.param == "?user=Not%20Connor&tag=Lactose-Free"):
        return {
            "data": {},
            "status": 200
        }
    else:
        return {"Not implemented": ":("}


@pytest.fixture(scope="session")
def DishesPost() -> dict:
    return {
        "data": "Commit successful!",
        "status": 200
    }


@pytest.fixture(scope="session")
def DishesDelete() -> dict:
    return {
        "data": "Deleted test dish successfully.",
        "status": 200
    }


@pytest.fixture(scope="session")
def UsersResponse(request) -> dict:
    if (request.param == "GET"):
        return {
            "data": [
                {
                    "id": 1,
                    "user_name": "Connor"
                },
                {
                    "id": 2,
                    "user_name": "Not Connor"
                }
            ],
            "status": 200
        }
    elif (request.param == "POST"):
        return {
            "data": "Added user Test User",
            "status": 200
        }
    elif (request.param == "DELETE"):
        return {
            "data": "Removed user Test User",
            "status": 200
        }
    return {"error": "Bad use of fixture!", "status": 400}


@pytest.fixture(scope="session")
def TagsResponse(request) -> dict:
    if (request.param == "GET"):
        return {
            "data": [
                {
                    "dish_name": "Chicken Shawarma Platter",
                    "id": 1,
                    "restaurant_name": "Ozzy's",
                    "tag": "Halal"
                },
                {
                    "dish_name": "Chicken Shawarma Wrap",
                    "id": 2,
                    "restaurant_name": "Shawarma Palace",
                    "tag": "Halal"
                },
                {
                    "dish_name": "Chicken Shawarma Platter",
                    "id": 3,
                    "restaurant_name": "Ozzy's",
                    "tag": "Lactose-Free"
                }
            ],
            "status": 200
        }
    elif (request.param == "POST"):
        return {
            "data": "Tag added successfully: test",
            "status": 200
        }
    elif (request.param == "DELETE"):
        return {
            "data": "Tag deleted successfully from: Chicken Shawarma Wrap",
            "status": 200
        }
    return {"error": "Bad use of fixture!", "status": 400}


@pytest.fixture(scope="session")
def LikesResponse(request) -> dict:
    if (request.param == "?dish_name=Chicken%20Shawarma%20Platter&restaurant_name=Ozzy's"):
        return {
            "data": [
                {
                    "dish_name": "Chicken Shawarma Platter",
                    "id": 1,
                    "restaurant_name": "Ozzy's",
                    "user_name": "Connor"
                }
            ],
            "status": 200
        }
    elif (request.param == "POST"):
        return {
            "data": "Connor liked Chicken Shawarma Wrap at Shawarma Palace.",
            "status": 200
        }
    elif (request.param == "DELETE"):
        return {
            "data": "Like successfully removed from Chicken Shawarma Wrap for user Connor.",
            "status": 200
        }
    return {"error": "Bad use of fixture!", "status": 400}
