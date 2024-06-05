from flask import request, render_template, current_app, Blueprint
from app.helpers import DBHelpers as db
from app.helpers import Translators as trans
from werkzeug.exceptions import BadRequest
import os

routes_blueprint: Blueprint = Blueprint('routes_blueprint', __name__)


@routes_blueprint.route("/")
def main_endpoint() -> dict:
    """
    Base endpoint, mostly to make sure the app is working.

    :returns: 200 code and text.
    """

    return {"data": "Main Endpoint!", "status": 200}


@routes_blueprint.route("/users", methods=["DELETE", "POST", "GET"])
def users() -> dict:
    """
    Create and Read for users table.

    :returns: 200 code and dictionary of users.
    :raises BadRequest: Raises error on improperly formatted request.
    """
    if (request.method == "GET"):
        return db.get("SELECT * FROM users;")

    user_name: str = request.json["user_name"] if request.data else None
    if (request.method == "POST"):
        db.commit(f"INSERT INTO users (user_name) VALUES (N'{user_name}');")
        return {"data": f"Added user {user_name}", "status": 200}

    raise BadRequest(
        "Improperly formatted request. This endpoint only takes GET, POST, or DELETE.")


@routes_blueprint.route("/users/<string:user_name>", methods=["DELETE"])
def delete_user(user_name: str) -> dict:
    """
    handles DELETE for users table.

    :param user_name: Name of the user to be deleted.
    :returns: dictionary confirming delete was successful, and 200 status code.
    """
    db.commit(f"DELETE FROM users WHERE user_name=N'{user_name}';")
    return {"data": f"Removed user {user_name}", "status": 200}


@routes_blueprint.route("/tags", methods=["POST", "GET"])
def tags() -> dict:
    """
    Create and Read for tags, though I don't really have need for an Update function so it's just CRD.
    Tags are in a one-to-many relationship with dishes (e.g. multiple dishes can be Halal or Lactose Free)

    :param dish_name: When POST requests are sent, you need a dish name to add.
    :param restaurant_name: When POST requests are sent, you need to specify the restaurant.
    :param tag: Tag name to filter by or write into DB. If GET: place in query params, else place in request body.
    """

    # Get requests expect query params for filters.
    if (request.method == "GET"):
        if ("tag" not in request.args):
            return db.get(f"SELECT * FROM tags;")
        else:
            request_tag: str | None = request.args.get('tag')
            if (isinstance(request_tag, str)):
                read_tag: str = trans.escape_string(
                    request_tag.replace(" ", "-"))
                return db.get(f"SELECT * FROM tags WHERE tag=N'{read_tag}'")

    # All other requests expect request body to carry info.
    dish_name: str = trans.escape_string(request.json['dish_name'])
    restaurant_name: str = trans.escape_string(request.json['restaurant_name'])
    tag: str = trans.escape_string(request.json['tag'].replace(" ", "-"))
    if (request.method == "POST"):
        db.commit(
            f"INSERT INTO tags (tag, dish_name, restaurant_name) VALUES (N'{tag}', N'{dish_name}', N'{restaurant_name}');")
        return {"data": f"Tag added successfully: {tag}", "status": 200}
    else:
        raise BadRequest(
            "Improperly formatted request. This endpoint only takes GET, POST, or DELETE.")


@routes_blueprint.route("/tags/<string:restaurant>/<string:dish>/<string:tag>", methods=["DELETE"])
def delete_tag(restaurant: str, dish: str, tag: str) -> dict:
    """
    Handles deleting tags.

    :param restaurant: Restaurant with the specific dish you're removing a tag from.
    :param dish: Dish you're removing the tag from.
    :param tag: Tag you're removing.
    :returns: confirmation on successful delete.
    """
    db.commit(
        f"DELETE FROM tags WHERE dish_name=N'{dish}' AND tag=N'{tag}' AND restaurant_name=N'{restaurant}';")
    return {"data": f"Tag deleted successfully from: {dish}", "status": 200}


@routes_blueprint.route("/likes", methods=["DELETE", "POST", "GET"])
def likes() -> dict:
    """
    CRD for what foods are liked by which users.

    :param dish_name: dish you wish to read likes from or add a like to.
    :param restaurant_name: what restaurant that dish is from.
    :param user_name: required if POSTing, user who liked the dish.
    :returns: dictionary containing all users who like the given dish, or confirmation of post.
    :raises BadRequest: on improper request formatting.
    """
    dish_name: str
    restaurant_name: str
    if (request.method == "GET"):
        dish_name = trans.escape_string(request.args.get('dish_name'))
        restaurant_name = trans.escape_string(
            request.args.get('restaurant_name'))
        return db.get(f"SELECT * FROM likes WHERE dish_name=N'{dish_name}' AND restaurant_name=N'{restaurant_name}';")

    dish_name = trans.escape_string(request.json['dish_name'])
    restaurant_name = trans.escape_string(request.json['restaurant_name'])
    user_name: str = trans.escape_string(request.json['user_name'])
    if (request.method == "POST"):
        db.commit(
            f"INSERT INTO likes (restaurant_name, dish_name, user_name) VALUES (N'{restaurant_name}', N'{dish_name}', N'{user_name}');")
        return {"data": f"{user_name} liked {dish_name} at {restaurant_name}.", "status": 200}
    else:
        raise BadRequest(
            "Improperly formatted request. This endpoint only takes GET, POST, or DELETE.")


@routes_blueprint.route("/likes/<string:restaurant>/<string:dish>/<string:user_name>", methods=["DELETE"])
def delete_like(restaurant: str, dish: str, user_name: str) -> dict:
    """
    Handles delete action for likes.
    :param user_name: user who is removing their like.
    :param dish: name of dish being disliked.
    :param restaurant: name of restaurant that dish is from.
    """
    current_app.logger.info(f"{restaurant} {dish} {user_name}")
    db.commit(
        f"DELETE FROM likes WHERE dish_name=N'{dish}' AND user_name=N'{user_name}' AND restaurant_name=N'{restaurant}';")
    return {"data": f"Like successfully removed from {dish} for user {user_name}.", "status": 200}


@routes_blueprint.route("/dishes", methods=["GET", "POST"])
def dishes() -> dict:
    """
    Methods for all dishes, regardless of tags or restaurant.

    :param tag: if GET, filters out any dishes without the given tag(s)
    :param user: if GET, filters out any dishes not liked by the given user(s)
    :param dish_name: if POST, name of dish being added.
    :param restaurant_name: if POST, name of restaurant dish is being added to.
    :returns: For GET, returns dict containing restaurants with each dish that meets filter criteria. For POST returns confirmation of successful post.
    :raises BadRequest: for improperly formatted requests.
    """

    if (request.method == "GET"):
        if ("tag" not in request.args and "user" not in request.args):
            no_filter_response: dict = db.get(f"""SELECT dishes.dish_name, tags.tag, likes.user_name, dishes.restaurant_name FROM dishes LEFT JOIN tags
                                    ON tags.dish_name = dishes.dish_name AND tags.restaurant_name = dishes.restaurant_name
                                    LEFT JOIN likes ON likes.restaurant_name = dishes.restaurant_name AND likes.dish_name = dishes.dish_name;""")
            all_dishes: dict = trans.wash_dishes(no_filter_response)
            return {"data": all_dishes, "status": 200}
        users: str
        filter_tags: str
        if ("tag" in request.args and "user" in request.args):
            users = ",".join(request.args.getlist('user'))
            filter_tags = ",".join(request.args.getlist('tag'))
            multi_filter_response: dict = db.get(f"""SELECT likes.dish_name, likes.user_name, tags.tag, likes.restaurant_name FROM likes INNER JOIN tags 
                                    ON tags.restaurant_name = likes.restaurant_name AND tags.dish_name = likes.dish_name AND find_in_set(tags.tag, N'{filter_tags}')
                                    WHERE find_in_set(likes.user_name, N'{users}');""")
            filtered_dishes: dict = trans.wash_dishes(multi_filter_response)
            return {"data": filtered_dishes, "status": 200}
        elif ("user" in request.args):
            users = ",".join(request.args.getlist('user'))
            likes_response: dict = db.get(f"""SELECT likes.dish_name, likes.user_name, tags.tag, likes.restaurant_name FROM likes LEFT JOIN tags 
                                    ON tags.restaurant_name = likes.restaurant_name AND tags.dish_name = likes.dish_name
                                    WHERE find_in_set(likes.user_name, N'{users}');""")
            liked_dishes: dict = trans.wash_dishes(likes_response)

            return {"data": liked_dishes, "status": 200}

        elif ("tag" in request.args):
            filter_tags = ",".join(request.args.getlist('tag'))
            tags_response: dict = db.get(f"""SELECT dishes.dish_name, tags.tag, likes.user_name, dishes.restaurant_name FROM dishes INNER JOIN tags
                                    ON tags.dish_name = dishes.dish_name AND tags.restaurant_name = dishes.restaurant_name
                                    LEFT JOIN likes ON likes.restaurant_name = dishes.restaurant_name AND likes.dish_name = dishes.dish_name
                                    WHERE find_in_set(tags.tag, N'{filter_tags}');""")
            # Group dishes by name
            tagged_dishes: dict = trans.wash_dishes(tags_response)

            return {"data": tagged_dishes, "status": 200}

        raise BadRequest("Unexpected request.")

    dish_name: str = trans.escape_string(request.json['dish_name'])
    restaurant: str = trans.escape_string(request.json['restaurant_name'])
    if (request.method == "POST"):
        db.commit(
            f"INSERT INTO dishes (dish_name, restaurant_name) VALUES (N'{dish_name}', N'{restaurant}');")

        if ("likes" in request.json):
            likes: list = request.json['likes']
            for user_name in likes:
                db.commit(
                    f"INSERT INTO likes (dish_name, user_name) VALUES (N'{dish_name}', N'{trans.escape_string(user_name)}');")
        if ("tags" in request.json):
            tags: list = request.json['tags']
            for tag in tags:
                db.commit(
                    f"INSERT INTO tags (name, dish_name) VALUES (N'{trans.escape_string(tag)}', N'{dish_name}')")
        return {"data": f"Commit successful!", "status": 200}

    else:
        raise BadRequest(
            "Improperly formatted request. This endpoint only takes GET, POST, or DELETE.")


@routes_blueprint.route("/restaurants/<string:restaurant>/<string:dish>", methods=["DELETE"])
def delete_dish(restaurant: str, dish: str):
    """
    Handles deleting for dishes.

    :param dish: Dish name being deleted.
    :param restaurant: Restaurant that has that dish.
    """
    db.commit(
        f"DELETE FROM likes WHERE dish_name=N'{dish}' AND restaurant_name=N'{restaurant}';")
    db.commit(
        f"DELETE FROM tags WHERE dish_name=N'{dish}' AND restaurant_name=N'{restaurant}';")
    db.commit(
        f"DELETE FROM dishes WHERE dish_name=N'{dish}' AND restaurant_name=N'{restaurant}';")
    return {"data": f"Deleted {dish} successfully.", "status": 200}


@routes_blueprint.route("/dishes/<string:tag>", methods=["GET"])
def dishes_by_tag(tag: str):
    """
    Returns all dishes with a given tag. Unused.
    """
    return db.get(f"SELECT * FROM dishes INNER JOIN tags ON tags.dish_name = dishes.dish_name;")


@routes_blueprint.route("/dishes/<string:restaurant>", methods=["GET"])
def dishes_by_restaurant(restaurant: str) -> dict:
    """
    Queries database for all dishes from a given restaurant name. Unused.

    :param restaurant: Name of the restaurant
    :returns: returns all dishes that restaurant offers
    :raises Exception: Raises errors for failures to connect to DB.
    """
    restaurant = trans.escape_string(restaurant)
    if (request.method == "GET"):
        return db.get(f"SELECT * FROM dishes WHERE restaurant_name = '{restaurant}';")

    else:
        raise BadRequest(
            "Improperly formatted request. This endpoint only takes GET requests.")


@routes_blueprint.route("/restaurants", methods=["GET", "POST", "PUT"])
def restaurants() -> dict:
    """
    Queries database for all restaurants.

    :returns: list of all restaurants.
    :raises Exception: Raises errors for failures to connect to DB.
    """

    restaurant_name: str | None = trans.escape_string(
        request.json['restaurant_name']) if request.data else None
    if (request.method == "GET"):
        return db.get("SELECT * FROM restaurants;")
    elif (request.method == "POST"):
        db.commit(
            f"INSERT INTO restaurants (restaurant_name) VALUES (N'{restaurant_name}');")
        return {"data": f"Commit successful!", "status": 200}
    elif (request.method == "PUT"):
        db.commit(
            f"UPDATE restaurants SET {trans.unpack_payload_update(request.json)} WHERE restaurant_name = N'{restaurant_name}';")
        return {"data": "Commit successful!", "status": 200}
    else:
        raise BadRequest("Improperly formatted request.")


@routes_blueprint.route("/restaurants/<string:restaurant>", methods=["DELETE"])
def delete_restaurant(restaurant: str) -> dict:
    """
    Handles deleting restaurants and all related data.

    :param restaurant: name of restaurant being deleted.
    :returns: Confirmation of successful delete.
    """
    db.commit(
        f"DELETE FROM likes WHERE restaurant_name = N'{restaurant}';")
    db.commit(
        f"DELETE FROM tags WHERE restaurant_name = N'{restaurant}';")
    db.commit(
        f"DELETE FROM dishes WHERE restaurant_name = N'{restaurant}';")
    db.commit(
        f"DELETE FROM restaurants WHERE restaurant_name = N'{restaurant}';")
    return {"data": "Delete successful!", "status": 200}


@routes_blueprint.route("/docs")
def docs():
    """
    Displays documentation using Swagger.io

    :returns: rendered html template of documentation.
    :raises Exception: for generic errors.
    """
    current_app.logger.debug(
        f"Template directory is: {current_app.template_folder}")
    for filename in os.listdir(current_app.template_folder):
        print(f"file: {filename}")
    try:
        return render_template('swaggerui.html')
    except Exception as e:
        current_app.logger.info("Failed to return docs.")
        return os.listdir(current_app.template_folder)
