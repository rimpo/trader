FROM python:3.8.3

# In order for the Docker build cache to cache packages installed via pip,
# it‚Äôs necessary to add the requirements.txt file to the image, and run pip install,
# before adding the rest of the repo.

# install ta-lib
RUN pip install numpy
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install
RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

COPY requirements.txt /app/backend/
RUN pip install -r /app/backend/requirements.txt
COPY . /app/backend

ARG KITE_API_KEY
ARG KITE_API_SECRET

ENV TRADER_RIMPO_ENV=production
ENV FLASK_APP=/app/backend/app.py

WORKDIR /app/backend
ENTRYPOINT ["/app/backend/bin/entrypoint.sh"]

