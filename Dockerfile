FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:alpine

RUN apk update && apk upgrade

RUN apk add python3

RUN command