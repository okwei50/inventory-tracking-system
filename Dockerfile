FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.11

RUN pip install psycopg2-binary --target ${LAMBDA_TASK_ROOT}

COPY lambda_function.py ${LAMBDA_TASK_ROOT}/

CMD ["lambda_function.lambda_handler"]
