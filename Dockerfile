FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    ffmpeg \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code

COPY ./requirements.txt .

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py39_24.1.2-0-Linux-x86_64.sh
RUN bash Miniconda3-py39_24.1.2-0-Linux-x86_64.sh -b -p /miniconda

# Add miniconda to the PATH
ENV PATH=/miniconda/bin:$PATH


RUN pip install -r requirements.txt  
RUN git config --global http.postBuffer 157286400
RUN git clone https://github.com/ggerganov/whisper.cpp.git


COPY . .

EXPOSE 14022

RUN mkdir -p uploads

CMD ["python", "app.py"]
