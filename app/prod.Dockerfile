# pull official base image
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user and group for running the application

# Create the application directory and set it as the working directory
WORKDIR /app



# Install system dependencies
RUN apk --no-cache add curl

# install dependencies
RUN pip install --upgrade pip

# Install pipenv globally
RUN pip install pipenv

# Copy only the Pipfiles first to leverage Docker caching
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv
RUN pipenv install  --system

# Copy the entry point script to the /app directory and set its permissions
COPY django-entrypoint.prod.sh /app/
RUN chmod +x /app/django-entrypoint.prod.sh



# Copy the entire project into the container
COPY . .

#RUN #mkdir -p /app/staticfiles && chmod 755 /app/staticfiles


# Expose any necessary ports
EXPOSE 8000

