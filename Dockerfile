FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create virtual env
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install

# Copy the rest of the code
COPY . .

# Expose port
EXPOSE 8000

# Run the app
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]