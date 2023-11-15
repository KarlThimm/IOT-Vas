FROM python:3

WORKDIR /usr/src/app

EXPOSE 5000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && rm requirements.txt

COPY app.py ./

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
