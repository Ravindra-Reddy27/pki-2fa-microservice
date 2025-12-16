# ############################
# # Stage 1: Builder
# ############################
# FROM python:3.11-slim AS builder

# WORKDIR /app

# # Copy dependency list first (for caching)
# COPY requirements.txt .

# # Install dependencies into a virtual location
# RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ############################
# # Stage 2: Runtime
# ############################
# FROM python:3.11-slim

# # Set timezone (CRITICAL)
# ENV TZ=UTC

# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         cron \
#         tzdata && \
#     rm -rf /var/lib/apt/lists/*

# # Configure timezone
# RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
#     echo UTC > /etc/timezone

# # Copy Python dependencies from builder
# COPY --from=builder /install /usr/local

# # Copy application code
# COPY app.py .
# COPY decrypt_seed.py .
# COPY totp_create_check.py .
# COPY student_private.pem .
# COPY instructor_public.pem .

# # Copy cron configuration
# COPY cron/2fa-cron /etc/cron.d/2fa-cron

# # Set correct permissions for cron
# RUN chmod 0644 /etc/cron.d/2fa-cron && \
#     crontab /etc/cron.d/2fa-cron

# # Create volume mount points
# RUN mkdir -p /data /cron && \
#     chmod 755 /data /cron

# # Expose API port
# EXPOSE 8080

# # Start cron + FastAPI
# CMD cron && uvicorn app:app --host 0.0.0.0 --port 8080




############################
# Stage 1: Builder
############################
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


############################
# Stage 2: Runtime
############################
FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        cron \
        tzdata && \
    rm -rf /var/lib/apt/lists/*

RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo UTC > /etc/timezone

COPY --from=builder /install /usr/local

# Application code
COPY app.py .
COPY decrypt_seed.py .
COPY totp_create_check.py .
COPY student_private.pem .
COPY instructor_public.pem .

# 🔴 CRITICAL: copy cron script
COPY scripts/log_2fa_cron.py /app/scripts/log_2fa_cron.py

# Cron configuration
COPY cron/2fa-cron /etc/cron.d/2fa-cron

RUN chmod 0644 /etc/cron.d/2fa-cron && \
    crontab /etc/cron.d/2fa-cron

RUN mkdir -p /data /cron && \
    chmod 755 /data /cron

EXPOSE 8080

CMD cron && uvicorn app:app --host 0.0.0.0 --port 8080
