
FROM python:3.8.2

COPY . /
COPY templative/lib/gameManager/template /

RUN pip3 install -r requirements.txt && \
    python3 setup.py install && \
    pip3 freeze && \
    python3 -V

CMD [ "python3", "./docker-source.py" ]