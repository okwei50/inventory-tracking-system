FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.11

COPY psycopg2/ ${LAMBDA_TASK_ROOT}/psycopg2/
COPY psycopg2_binary.libs/ ${LAMBDA_TASK_ROOT}/psycopg2_binary.libs/
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/

CMD ["lambda_function.lambda_handler"]
