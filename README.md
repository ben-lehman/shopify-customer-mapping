# shopify-customer-mapping
This is an in progress Flask that creates an API containing generalized Shopify customer location data to be accessed by a LeafletJS frontend. Currently the build handles the API creation and Shopify data extraction. The routes on the app are used as a admin dashboard to update, view, and clear the API data.

## Installation
To fully run this app you need to create a Shopify private app and then create env variables based off of the credentials provided. This app isn't fully ready to run independent of the context I'm using it in, but if you'd like to try to get it running you can follow the directions below.

1. Clone this repo to your local machine `git clone https://github.com/ben-lehman/flaskr-tutorial.git`
2. Initialize a virtualenv and the activicate the virtualenv using `source venv/bin/activate`
3. Install requirements with `pip install -r requirements.txt`
4. Set up env variables stated in config.py
3. Set the app location and enviroment:
```
$ export FLASK_APP=app
$ export FLASK_ENV=development
```
4. Initialize the database `$ flask db upgrade`
5. Run the app `flask run`

The app should be running at http://localhost:5000/

## Notes and Todos

1. There are currently a few half-baked features in this repo. One being the ability to PUT the api data directly into the Shopify client so that the frontend doesn't have to make an API request.
2. TODO: Set up celery to handle the initial data request from Shopify
3. Build out a proper admin dashboard to handle updates
4. Automate data update tasks so a Heroku worker can run them on a schedule
