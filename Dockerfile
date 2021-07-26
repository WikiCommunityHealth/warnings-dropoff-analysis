# Docker image
FROM python:3.9.2
# Environment
ENV YOUR_ENV=${YOUR_ENV} \
  POETRY_VERSION=1.0.0 \
  MONGODB_URI=mongodb://127.0.0.1:27017
# Poetry
RUN pip install "poetry==$POETRY_VERSION"
# Work directory
WORKDIR /usr/src/app
# dotenv
RUN echo "MONGODB_URI=$MONGODB_URI" > .env
# Installing brew
RUN apt-get update && \
  apt-get install -y -q --allow-unauthenticated \
  build-essential \
  procps \
  curl \
  file \
  git \
  gzip \
  tar \
  p7zip-full \
  sudo
RUN useradd -m -s /bin/zsh linuxbrew && \
  usermod -aG sudo linuxbrew &&  \
  mkdir -p /home/linuxbrew/.linuxbrew && \
  chown -R linuxbrew: /home/linuxbrew/.linuxbrew
USER linuxbrew
# brew
RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
# Add brew to PATH
ENV PATH="/home/linuxbrew/.linuxbrew/bin:${PATH}"
# Installing parallel
RUN brew install parallel
# Creating folders, and files
USER root
COPY . .
# Installing dependencies
RUN make install
# Making the run.sh executable
RUN chmod +x run.sh
# Run the run script
CMD ./run.sh