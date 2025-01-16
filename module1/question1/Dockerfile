FROM python:3.12.8

# specify work directory
WORKDIR /app

RUN python -m venv /venv
ENV PATH=/venv/bin:$PATH VIRTUAL_ENV=/venv

# Question 1 entrypoint is bash only
ENTRYPOINT [ "bash" ]
