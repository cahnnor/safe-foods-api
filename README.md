# What is Safe Foods?

Safe foods is a self-hosted app developed to streamline the process of deciding where to eat, especially when working with a group of people who have varying dietary restrictions due to chronic illness or religious beliefs.

This API handles the data for places the group has eaten, what dishes have been tried and who can eat them. Data is stored primarily by restaurant, grouping data on each individual dish they offer as well as tags for additional data like if they have delivery or what apps their food can be ordered from (e.g: Uber Eats).

# How this API works:

This API is built in Python using Flask. This was chosen since the API primarily focuses on querying and grouping data from a database, so it doesn't have to do a lot of heavy lifting. The plan is to use this in part of a larger application, so authentication has taken a back-seat for now.

Development is streamlined using Docker-Compose to spin up a DB image for the API, and Pytest to run unit tests and Mypy for static analysis. The logic is broken out into a few files: `routes.py` which builds all of the API's routes and methods, `helpers.py` which contains a few helpful functions for the DB and for manipulating data, and `handlers.py` to handle errors (very minimally for the time being).

The main functionality of the API is to edit the following tables:
- `users` - What people you typically eat with.
- `restaurants` - What restaurants your group has eaten at.
- `dishes` - What foods you've tried at those restaurants.
- `tags` - categories to filter dishes by (e.g. Lactose-Free or Gluten-Free). Relates to dishes.
- `likes` - Which foods are liked by which users.

The schema may be a little more detailed than necessary for the project as it stands, but I wanted to set it up to leave the option open in the future to expand upon this project in any direction.

## Running Locally:

To test out the API you can spin it up with `make start` and `make setup` then test it with postman or your browser at `localhost:5000`, and run `make down` to remove it or `make restart` to stop, rebuild, and restart the containers. The makefile also has a couple of helpful tools for developing. 

### Debugging tools
- `make format-check` - runs autopep8 on all python files to diff code standards to see if they follow pep8 standards.
- `make format-fix` - alters all code to follow pep8 standards, if you don't want to do it yourself.
- `make type-check` - runs mypy on all files to perform static analysis.

### The docs

To view the documentation for this API clone and start the API locally as outlined above and go to the endpoint `localhost:5000/docs`. This API is documented in Swagger, following the OpenAPI v3.1.0 specification.

# Up next:

## For this repo:

The upcoming updates for this API will be some small tweaks mainly:
- Add a filter for the dishes search that only allows results within a certain distance or delivery time.
- Paginate responses.
- Implement full-flow tests.
- Add the ability to pull from the UberEats API for data near the user.

## Outside of this repo:

- Setting up an example frontend project in React.js to demonstrate a full working safe-foods app.
- Create a repo for managing schema changes rather than holding them in the migrations folder.
- Create an all-in-one development environment using minikube to host all repos in a production-like environment.
- Productionize the app for demo purposes.