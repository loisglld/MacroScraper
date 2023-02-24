# Step 1: Use an official Python image as a parent image
FROM python:3.11

# Step 2: Define the working directory in the container
WORKDIR /app

# Step 3: Copy the code of your project into the container
COPY . .
# Step 4: Install dependencies of your project
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Define the entry point of your application
CMD [ "python", "./src/Main.py" ]
