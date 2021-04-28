FROM python:3.8
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY cc_sched/* /cc_sched/
CMD ["gunicorn","-b","0.0.0.0:80","-k","uvicorn.workers.UvicornWorker","--forwarded-allow-ips","*","--proxy-allow-from","*","cc_sched.app:app"]
