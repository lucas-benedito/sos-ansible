FROM python:3

WORKDIR /home/ansible
RUN useradd -m ansible && chown ansible:ansible /home/ansible
USER ansible
ENV IS_CONTAINER=True
COPY requirements.txt ./
RUN pip install pip --upgrade && pip install --no-cache-dir -r requirements.txt

COPY ./sos_ansible .
ENTRYPOINT [ "python", "main.py" ]
