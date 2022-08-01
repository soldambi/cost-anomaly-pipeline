FROM public.ecr.aws/bitnami/python:3.10.0

RUN pip --no-cache-dir install boto3 awswrangler pyathena pymysql sqlalchemy pandas scikit-learn scipy pmdarima statsmodels

COPY preprocessing.py /app/preprocessing.py
COPY arima.py /app/arima.py
COPY ets.py /app/ets.py
COPY pca.py /app/pca.py
COPY pcr.py /app/pcr.py
