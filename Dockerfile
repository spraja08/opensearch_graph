FROM python:3.9 
# Or any preferred Python version.
ADD *.py ./
ADD root-ca.pem ./
COPY requirements.txt /tmp/requirements.txt
EXPOSE 5001
RUN python3 -m pip install -r /tmp/requirements.txt
CMD python3 -m flask_app opensearch
# Or enter the name of your unique directory and parameter set.