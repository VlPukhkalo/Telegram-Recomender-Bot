FROM python
WORKDIR /app
COPY requirements.txt /app
RUN python -m pip install -r requirements.txt

COPY . /app

CMD ["python", "app.py"]