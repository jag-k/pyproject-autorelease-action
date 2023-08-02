FROM python:3.11-buster

WORKDIR /

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

ENTRYPOINT ["python", "-m", "pyproject_autorelease_action"]
