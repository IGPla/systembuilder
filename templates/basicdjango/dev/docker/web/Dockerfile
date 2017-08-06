FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /project/code
WORKDIR /project/code
RUN apt-get update
ADD common_systemrequirements.txt /project/code/
ADD project_systemrequirements.txt /project/code/
RUN xargs apt-get install -y < common_systemrequirements.txt
RUN xargs apt-get install -y < project_systemrequirements.txt
ADD common_requirements.txt /project/code/
ADD project_requirements.txt /project/code/
RUN pip install -r common_requirements.txt
RUN pip install -r project_requirements.txt