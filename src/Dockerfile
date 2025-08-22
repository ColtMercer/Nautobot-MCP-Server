FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Copy project metadata and package for installation (build with -f src/Dockerfile .)
COPY src/pyproject.toml ./pyproject.toml
COPY README.md ./README.md
COPY src/nautobot_mcp_server ./nautobot_mcp_server

# Install Python package and dependencies
RUN pip install --no-cache-dir .

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 app && chown -R app:app /app
USER app

# Expose port
EXPOSE 7001

# Run the application
CMD ["python", "-m", "nautobot_mcp_server.server"]
