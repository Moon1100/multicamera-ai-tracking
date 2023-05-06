FROM python:3.9.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# RUN pip3 install --no-cache-dir dlib

# Set the working directory to /app
WORKDIR /web_face_detection

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required packages
RUN pip3 install -r requirements.txt

# Copy the entire project to the container
COPY . .

# Run the main script


# CMD ["python3", "web5.py"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
