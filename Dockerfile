FROM python:3.11-slim

# Install miniconda
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add conda to path
ENV PATH /opt/conda/bin:$PATH

# Copy environment.yml
COPY venv/environment.yml /app/environment.yml

# Create conda environment
RUN conda env create -f /app/environment.yml

# Set up conda environment activation
SHELL ["/bin/bash", "-c"]
RUN echo "source activate mcp-server" > ~/.bashrc
ENV PATH /opt/conda/envs/mcp-server/bin:$PATH

# Set working directory
WORKDIR /app

# Copy application code
COPY src/ /app/src/
# COPY .env /app/.env

# Set Python path
ENV PYTHONPATH="/app/src"

# Expose port
EXPOSE 3000

# Run the application
CMD ["python", "/app/src/server.py"] 