import pymysql
import os
from flask import current_app


class DBHelpers:
    @staticmethod
    def commit(query: str) -> None:
        """
        Helper function to execute and commit a query on the database.

        :param query: Query to execute, can be any update or put query.
        :returns: Nothing on success.
        :raises Exception: Raises an error for a failed connection.
        """

        try:
            with pymysql.connect(host="db",  # May need to change when DB moves, not best practice...
                                 port=3306,
                                 user="root",
                                 password=os.environ['MYSQL_PASSWORD'],
                                 database="food",
                                 cursorclass=pymysql.cursors.DictCursor,
                                 client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS) as connection:
                with connection.cursor() as cursor:
                    # Add a check for if element already exists?
                    cursor.execute(query)
                    connection.commit()
            return
        except Exception as e:
            current_app.logger.error(f"Failed commit to DB, see error: {e}")
            raise Exception(f"Commit failed.")

    @staticmethod
    def get(query: str) -> dict:
        """
        Helper function to execute and commit a query on the database.

        :param query: Query to execute, can be any SELECT query.
        :returns: Nothing on success.
        :raises Exception: Raises an error for a failed connection.
        """

        try:
            with pymysql.connect(host="db",  # May need to change when DB moves, not best practice...
                                 port=3306,
                                 user="root",
                                 password=os.environ['MYSQL_PASSWORD'],
                                 database="food",
                                 cursorclass=pymysql.cursors.DictCursor,
                                 client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()
            return {"data": result, "status": 200}
        except Exception as e:
            current_app.logger.error(f"Failed to read db. Error {e}")
            raise Exception("Connection to DB failed.")


class Translators:
    @staticmethod
    def unpack_payload_update(payload: dict) -> str:
        """
        Converts the request.json object to a string of the format KEY1=VALUE1, KEY2=VALUE2, ...
        This way we can unpack requests for sql queries.

        :param payload: dictionary object, result of request.json.
        :returns: string of comma separated key = value pairs to fit into an UPDATE query.
        :raises Exception: On incorrectly formatted json data
        """
        output_list: list = []
        try:
            for key in payload.keys():
                if (key != 'restaurant_name' and key != 'name'):
                    output_list.append(f"{key}={payload[key]}")
        except Exception as e:
            raise Exception(
                f"Failed to read json data. Exception: {e}\n Payload: {payload}")
        return ",".join(output_list)

    @staticmethod
    def wash_dishes(response: dict) -> dict:
        """
        Sorts dishes by restaurant, looping in likes and tags data (e.g. Tag or Like), connected to a user name.
        If no field is given,

        :param response: list of dishes to sort
        :returns: Sorted list of dishes grouped by restaurant, displaying likes and tags for each dish.
        """

        restaurants: dict = {}
        for dish in response['data']:
            current_app.logger.info(dish)
            name: str = dish['dish_name']
            restaurant: str = dish['restaurant_name']

            # Restaurant not in dict.
            if (restaurant not in restaurants):
                restaurants[restaurant] = {"dishes": {
                    name: {"tags": [dish['tag']], "likes": [dish['user_name']]}}}

            else:
                # Dish is not in dict for this restaurant yet..
                if (name not in restaurants[restaurant]["dishes"]):
                    restaurants[restaurant]["dishes"][name] = {
                        "tags": [dish['tag']], "likes": [dish['user_name']]}

                # Dish is in dict, but tag isn't.
                if (dish['tag'] not in restaurants[restaurant]["dishes"][name]['tags']):
                    restaurants[restaurant]["dishes"][name]['tags'].append(
                        dish['tag'])

                # Tag is in dict, but likes aren't.
                if (dish['user_name'] not in restaurants[restaurant]["dishes"][name]['likes']):
                    restaurants[restaurant]["dishes"][name]['likes'].append(
                        dish['user_name'])

        return restaurants

    @staticmethod
    def escape_string(text: str | None) -> str:
        """
        Used for unpacking strings from user requests and making sure they're safe for an SQL query.

        :param text: the string to escape (e.g. Ozzy's)
        :returns: the string with escape characters (e.g. Ozzy\'s),

        :raises TypeError: in the event that the argument text is the wrong type.
        """
        translate_table = str.maketrans({"-": r"\-", "]": r"\]", "\\": r"\\", "^": r"\^",
                                         "$": r"\$", "*": r"\*", ".": r"\.", "'": r"\'", "(": r"\(", ")": r"\)"})

        if (isinstance(text, str)):
            return text.translate(translate_table)
        else:
            raise TypeError(f"Argment {text} could not be translated.")
