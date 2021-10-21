FROM 763104351884.dkr.ecr.us-west-2.amazonaws.com/pytorch-inference-neuron:1.7.1-neuron-py36-ubuntu18.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/tmp* \
    && apt-get clean

RUN pip install ffmpeg-python

COPY app/ /workspace
WORKDIR /workspace 
RUN chmod +x /workspace/entrypoint.sh
ENTRYPOINT ["/workspace/entrypoint.sh"]