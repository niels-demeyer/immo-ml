### immo-ml
This machine learning project aims to predict house prices on the Belgian market by scraping the data from [immoweb](https://www.immoweb.be/).

### usage 
1. Install [PostgreSQL](https://www.postgresql.org/), [Airflow](https://airflow.apache.org/) and docker [Docker](https://www.docker.com/) on your machine.
2. make an .env file with the following:
   ```
   DB_NAME=YourDB
   DB_HOST=YourHost
   DB_PORT=YourPort
   DB_USER=YourUser
   DB_PASS=YourPassword
   ```
3. Build the docker images with your environment variables:
   `docker build --build-arg DB_NAME=YourDB --build-arg DB_HOST=YourHost --build-arg DB_PORT=YourPort --build-arg DB_USER=YourUser --build-arg DB_PASS=YourPassword -t immo-hrequest -f docker-hrequest .`
   `docker build --build-arg DB_NAME=YourDB --build-arg DB_HOST=YourHost --build-arg DB_PORT=YourPort --build-arg DB_USER=YourUser --build-arg DB_PASS=YourPassword -t immo-most-expensive -f docker-most-expensive .`
4. Drop the DAGS into your airflow instance
   `DAGS/immo_most_expensive_dag.py`
   `DAGS/immo_hrequest_dag.py`
   


