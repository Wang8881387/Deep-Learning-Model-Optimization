FROM python:3.9
WORKDIR /app
COPY SNN0417 /app
RUN pip install pandas
RUN pip install imageio
RUN pip install matplotlib
EXPOSE 300

