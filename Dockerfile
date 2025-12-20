FROM python:3.9-slim
RUN pip install flask
RUN useradd -m appuser
USER appuser
WORKDIR /home/appuser
EXPOSE 3000
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
