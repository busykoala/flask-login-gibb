FROM frolvlad/alpine-python3

# Install bash, curl and host
RUN apk update
RUN apk add bash
RUN apk add curl
RUN apk add bind-tools

WORKDIR /app
COPY . .

# Touch the log file
RUN touch $(cat .env | grep LOG_PATH | cut -d "=" -f 2 | sed -e 's/^"//' -e 's/"$//')

# Setup application
RUN python setup.py install

# Setup database
RUN flask db init
RUN flask db migrate -m "users table"
RUN flask db upgrade
RUN flask seed run

# Expose port 5000 (default flask port)
EXPOSE 5000

# Run app
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]