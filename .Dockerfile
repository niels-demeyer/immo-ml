# Use an official Python runtime as a parent image
FROM python:3.12.3

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory to /app/scrapy/immoweb
WORKDIR /app/scrapy/immoweb

# Run scrapy crawl most_expensive -o output.json when the container launches
CMD ["scrapy", "crawl", "most_expensive", "-o", "output.json"]