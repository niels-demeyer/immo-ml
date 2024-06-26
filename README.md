# immo-ml🏡

This machine learning project aims to predict house prices on the Belgian market by scraping the data from [immoweb](https://www.immoweb.be/).

## setup

### installation requirements 📦

- Make sure you have PostgreSQL installed on your machine. [visit this link to install](https://www.postgresql.org/docs/current/tutorial-install.html)
- Make sure you have Python 3.8 installed on your machine. [visit this link to install](https://www.python.org/downloads/)
- Make sure you have pip installed on your machine. [visit this link to install](https://pip.pypa.io/en/stable/installing/)
- Make sure you have Docker installed on your machine. [visit this link to install](https://docs.docker.com/get-docker/)
- Make sure you have Docker Compose installed on your machine. [visit this link to install](https://docs.docker.com/compose/install/)
- Make sure you have airflow installed on your machine. [visit this link to install](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html)

### installation 🚀

### environment variables 🔑

1. make an .env file with the following credentials for your PostgreSQL database:

   ```
   DB_NAME=YourDB
   DB_HOST=YourHost
   DB_PORT=YourPort
   DB_USER=YourUser
   DB_PASS=YourPassword
   ```

### docker 🐋

You can also run the project with docker. Make sure to build the images with your environment variables as build arguments.

Build the docker images with your environment variables:
`docker build --build-arg DB_NAME=YourDB --build-arg DB_HOST=YourHost --build-arg DB_PORT=YourPort --build-arg DB_USER=YourUser --build-arg DB_PASS=YourPassword -t immo-hrequest -f docker-hrequest .`

`docker build --build-arg DB_NAME=YourDB --build-arg DB_HOST=YourHost --build-arg DB_PORT=YourPort --build-arg DB_USER=YourUser --build-arg DB_PASS=YourPassword -t immo-most-expensive -f docker-most-expensive .`

### python virtual environment 🐍

1. Create a virtual environment with Python 3.8:
   `python3 -m venv venv`
2. Activate the virtual environment:
   `source venv/bin/activate`
3. Install the requirements:
   `pip install -r requirements.txt`

## run the project 🚀

### airflow 🌬️

You can run the project with airflow. Make sure to have the airflow scheduler and webserver running. You can then copy the dags in the dags folder to your airflow dags folder. The dags will run in a Docker container and scrape the data from immoweb and store it in your PostgreSQL database.

- immo_most_expensive_dag.py: This dag will scrape the data from the immoweb website and store it in your PostgreSQL database.
- immo_hrequest_dag.py: This dag will scrape the data from the individual immoweb pages and store it in your PostgreSQL database.

### machine learning 🤖

You can run the machine learning model by running the following command:

- `python3 ml/preprocess.py`
- `python3 ml/train.py`
- `python3 ml/predict.py`
