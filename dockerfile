# Ubuntu containing updated apt and python/pip3
# ECR must be authenticated before use
FROM 003195358776.dkr.ecr.us-east-2.amazonaws.com/expense_tracker_ecr:python-base

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]
CMD [ "-m", "messaging_system.server" ]