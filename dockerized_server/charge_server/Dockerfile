FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1





WORKDIR /backend


# Install Python dependencies
COPY requirements.txt /backend/
RUN pip install -r requirements.txt

# Copy the rest of the Django project
COPY . /backend/

EXPOSE 8000