FROM python:3.9-slim

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip 

# Add this line to install nano
RUN apt-get update && apt-get install -y nano


# Add this line to install curl
RUN apt-get install -y curl


# Add this line to install psql
RUN apt-get install -y postgresql-client

# Add this line to install ping
RUN apt-get update && apt-get install -y iputils-ping

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "start.sh"]
