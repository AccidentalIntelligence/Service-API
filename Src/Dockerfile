# Use an official Python runtime as a parent image
FROM python:2.7

# Set the working directory to /app
WORKDIR /app

RUN apt-get update && apt-get install python-mysqldb

COPY ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 4443

# Run app.py when the container launches
ENTRYPOINT ["python", "API.py"]
