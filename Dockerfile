# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Install Scrapy
RUN pip install scrapy python-dotenv psycopg2-binary

# Copy the current directory contents into the container at /app
COPY . /app

# Change the working directory to /app/scrapy/immoweb
WORKDIR /app/scrapy/immoweb

# Run scrapy crawl most_expensive when the container launches
CMD ["scrapy", "crawl", "most_expensive"]