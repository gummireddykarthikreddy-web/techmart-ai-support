# Use a lightweight Python environment
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the backend code into the container
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Command to start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]