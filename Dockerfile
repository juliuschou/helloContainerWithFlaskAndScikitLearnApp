FROM python:3.8

ARG VERSION

LABEL org.label-schema.version=$VERSION

COPY ./california_housing_prediction.joblib /webapp/california_housing_prediction.joblib

COPY ./requirements.txt /webapp/requirements.txt

WORKDIR /webapp

RUN pip install -r requirements.txt

COPY webapp/* /webapp

ENTRYPOINT ["python"]

CMD ["app.py"]
