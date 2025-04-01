# Step 1: Use a lightweight Python image
FROM python:3.10-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy your application files into the container
COPY ./app /app

# Step 4: Install required Python packages
RUN pip install qrcode[pil]

# Step 5: Run the script when the container starts
CMD ["python", "generate_qr.py"]
