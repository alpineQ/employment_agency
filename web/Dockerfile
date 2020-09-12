FROM python:3.8.3-alpine

WORKDIR /app/

RUN apk add gcc g++ unixodbc unixodbc-dev curl

RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.5.2.2-1_amd64.apk
RUN apk add --allow-untrusted msodbcsql17_17.5.2.2-1_amd64.apk


COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
