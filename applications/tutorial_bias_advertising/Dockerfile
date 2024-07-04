FROM registry.access.redhat.com/ubi9/python-39

WORKDIR /app
RUN chgrp -R 0 /app && chmod -R g=u /app


COPY --chown=1001:0 requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY --chown=1001:0 . .

# Download and extract the dataset
RUN curl -OL https://dax-cdn.cdn.appdomain.cloud/dax-bias-in-advertising/1.0.0/bias-in-advertising.tar.gz \
    && tar -zxvf bias-in-advertising.tar.gz

EXPOSE 8080

CMD ["python", "app.py"]
