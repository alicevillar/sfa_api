# Here a new container will be created using Docker syntax
# Create a container to run the API from a simple container (Python 3)

# Setting the base container (the simplest)
FROM python:3.8
# Specifying that from now on everything will be stored inside the app
WORKDIR /app
# Pointing out that all files will be copied
# Copy has two parameters (source and destination)
# The first parameter says everything will be copied. The second says it will all be saved in the main file.
COPY . .
# Running three commands - Preparing the container so that the db can work
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/debian/8/prod.list > /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update \
 && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
 && ACCEPT_EULA=Y apt-get install -y mssql-tools \
 && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
 && source ~/.bashrc \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev -y \
 && apt install python3-openssl -y

# Installing the libraries
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["server.py"]



