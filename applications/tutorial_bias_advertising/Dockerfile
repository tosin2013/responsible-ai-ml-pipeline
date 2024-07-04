FROM registry.access.redhat.com/ubi9/python-39

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Download and extract the dataset
RUN curl -OL https://dax-cdn.cdn.appdomain.cloud/dax-bias-in-advertising/1.0.0/bias-in-advertising.tar.gz \
    && tar -zxvf bias-in-advertising.tar.gz

CMD ["python", "app.py"]
