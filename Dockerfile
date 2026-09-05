FROM python:3.11-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show Python output immediately
ENV PYTHONUNBUFFERED=1


# --------------------------------------------------
# INSTALL SYSTEM DEPENDENCIES
# --------------------------------------------------

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


# --------------------------------------------------
# SET WORKING DIRECTORY
# --------------------------------------------------

WORKDIR /app


# --------------------------------------------------
# COPY REQUIREMENTS FIRST
# --------------------------------------------------

COPY requirements.txt .


# --------------------------------------------------
# INSTALL PYTHON PACKAGES
# --------------------------------------------------

RUN pip install --no-cache-dir -r requirements.txt


# --------------------------------------------------
# COPY PROJECT FILES
# --------------------------------------------------

COPY . .


# --------------------------------------------------
# STREAMLIT CONFIGURATION
# --------------------------------------------------

EXPOSE 8501


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]