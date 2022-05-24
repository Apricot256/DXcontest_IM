FROM nvcr.io/nvidia/l4t-tensorflow:r34.1.0-tf1.15-py3

RUN apt-get update -y && apt-get upgrade -y && apt install -y openssh-client

RUN pip3 install Pillow opencv-python paho-mqtt requests

WORKDIR /root

CMD [ "python3" , "python/predict.py"]
