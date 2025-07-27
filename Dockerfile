FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock /app/

# Create a virtual environment and activate it
ENV UV_PROJECT_ENVIRONMENT="/opt/venv"
RUN uv sync --no-cache

# Add the virtual environment's bin to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application into the container.
COPY . .

# Run the application.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]