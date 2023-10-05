FROM python:3.10

RUN mkdir -p /home/app

COPY . /home/app

EXPOSE 5000

ENV NAME World

WORKDIR /home/app

RUN make install

# Run main.py when the container launches
CMD ["python", "src/UserAuthentication.py"]