FROM python:3.8.2-slim
COPY . /
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]