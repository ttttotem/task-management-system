# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

COPY pyproject.toml uv.lock /src/

# Create a virtual environment and activate it
ENV UV_PROJECT_ENVIRONMENT="/opt/venv"
RUN uv sync --locked --no-cache


RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" VIRTUAL_ENV="/opt/venv"

FROM python:${PYTHON_IMAGE_VERSION}-slim-bookworm


# Copy the application code
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
