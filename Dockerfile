FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python setup.py
ENTRYPOINT ["python"]
CMD ["server.py"]
