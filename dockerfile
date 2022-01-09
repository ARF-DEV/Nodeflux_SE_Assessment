# set image
FROM python:3.8.12-bullseye

# set working dir
WORKDIR /app

# install dependecies
COPY requirement.txt .
RUN pip install -r requirement.txt

# copy project directory
COPY . .

CMD [ "python", "src/app.py" ]