FROM python:3.14.0a3-alpine3.20

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Add non-root user and set ownership
RUN adduser -D app_user \
    && chown -R app_user:app_user /app

# Switch to non-root user
USER app_user

# Run the application
CMD ["python", "app.py"]
