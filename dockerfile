ARG language

FROM ubuntu AS base
RUN apt update -y
RUN mkdir /home/doron
WORKDIR /home/doron

FROM base as branch-version-python
RUN apt install python -y
COPY ./scripts/pyfile.py .
ENTRYPOINT ["python", "./pyfile.py"]

FROM base as branch-version-bash
COPY ./scripts/bashfile.sh .
ENTRYPOINT ["bash", "./bashfile.sh"]

FROM base as branch-version-all
RUN apt install python -y
COPY ./scripts/pyfile.py .
COPY ./scripts/bashfile.sh .
COPY ./scripts/allscripts.sh .
ENTRYPOINT ["bash", "./allscripts.sh"]

FROM branch-version-${language} AS final
