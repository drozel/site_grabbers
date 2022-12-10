FROM python:3.9 

COPY src grabber

RUN cd grabber && \
    pip install -r requirements.txt

ENTRYPOINT ["./grabber/run.sh"]
