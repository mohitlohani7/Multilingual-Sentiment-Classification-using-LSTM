# 1. Base Image (Python 3.9 Slim version for smaller size)
FROM python:3.9-slim

# 2. Set Working Directory
WORKDIR /app

# 3. Copy Requirements first (Caching ke liye)
COPY requirements.txt .

# 4. Install Dependencies
# --no-cache-dir keeps the image small
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the code
COPY . .

# 6. Expose Ports
# 8000 for FastAPI, 8501 for Streamlit
EXPOSE 8000
EXPOSE 8501

# 7. Command to run BOTH services using a script
# Hum ek trick use karenge taaki ek hi container mein dono chalein
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]