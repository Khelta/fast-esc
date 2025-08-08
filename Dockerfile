FROM python:3.13


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY fastesc /code/fastesc


CMD ["fastapi", "run", "fastesc/main.py", "--port", "80"]