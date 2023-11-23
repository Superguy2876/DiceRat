# Use an official Python runtime as a parent image
FROM python:slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Update pip and Install any needed packages specified in requirements.txt
# Force pip to ignore the Python version requirements of packages
RUN pip install --upgrade pip && pip install --ignore-requires-python --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]