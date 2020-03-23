FROM python:3.8.2
ADD lib lib
COPY lib/gameManager/template /
COPY cli.py /cli.py
ADD requirements.txt /
RUN pip3 install -r requirements.txt
RUN pip3 freeze
RUN python3 -V
# RUN pip install xml csv os sys tempfile re json
CMD [ "python3", "./cli.py", "produce" ]