# immo-ml

This machine learning project aims to predict house prices on the Belgian market by scraping the data from [immoweb](https://www.immoweb.be/).

## environment variables

1. make an .env file with the following:

   ```
   DB_NAME=YourDB
   DB_HOST=YourHost
   DB_PORT=YourPort
   DB_USER=YourUser
   DB_PASS=YourPassword
   ```

2. Build the docker images with your environment variables:
   `docker build --build-arg DB_NAME=YourDB --build-arg DB_HOST=YourHost --build-arg DB_PORT=YourPort --build-arg DB_USER=YourUser --build-arg DB_PASS=YourPassword -t immo-hrequest -f docker-hrequest .`

   `docker build --build-arg DB_NAME=YourDB --build-arg DB_HOST=YourHost --build-arg DB_PORT=YourPort --build-arg DB_USER=YourUser --build-arg DB_PASS=YourPassword -t immo-most-expensive -f docker-most-expensive .`
