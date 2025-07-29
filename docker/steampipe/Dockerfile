FROM debian:bullseye

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl unzip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Add steampipe user
ARG STEAMPIPE_USER_UID=1000
ARG STEAMPIPE_USER_GID=1000
RUN groupadd -g ${STEAMPIPE_USER_GID} steampipe && \
    useradd -m -u ${STEAMPIPE_USER_UID} -g steampipe steampipe

# Install Steampipe
RUN /bin/sh -c "$(curl -fsSL https://steampipe.io/install/steampipe.sh)"

# Switch to non-root user
USER steampipe

# Set default working directory
WORKDIR /home/steampipe

