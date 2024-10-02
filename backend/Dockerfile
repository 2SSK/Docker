# First stage: builder
FROM python:3.12-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy only the pyproject.toml first to leverage Docker cache
COPY pyproject.toml requirements.txt ./

# Install build dependencies and create wheels
RUN pip install --no-cache-dir wheel setuptools
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

# Copy the application source code
COPY src/ ./src/

# Create wheels for the project
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels .

# Second stage: runner
FROM python:3.12-slim AS runner

# Set the working directory in the final image
WORKDIR /app

# Copy wheels from the builder stage
COPY --from=builder /app/wheels /wheels

# Install the wheels and clean up
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.mysite.main:app", "--host", "0.0.0.0", "--port", "8000"]
