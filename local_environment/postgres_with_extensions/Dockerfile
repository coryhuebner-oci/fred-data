FROM postgres:17.4-alpine

# A Postgres image that includes additional extensions installed (e.g. pg_partman)

ENV PG_PARTMAN_VERSION v5.2.4

# Get minimal fetch dependencies named '.fetch-deps' for easier removal later
RUN apk add --no-cache --virtual .fetch-deps \
    ca-certificates \
    openssl \
    tar

# Get minimal build dependencies named '.build-deps' for easier removal later
RUN apk add --no-cache --virtual .build-deps \
    autoconf \
    automake \
    g++ \
    clang19 \
    llvm19 \
    libtool \
    libxml2-dev \
    make \
    perl \
    build-base \
    musl-dev \
    postgresql-dev

# Install pg_partman
RUN set -ex \
    # Download pg_partman
    && wget -O pg_partman.tar.gz "https://github.com/pgpartman/pg_partman/archive/$PG_PARTMAN_VERSION.tar.gz" \
    # Create a folder to put the src files in 
    && mkdir -p /usr/src/pg_partman \
    # Extract the src files
    && tar \
        --extract \
        --file pg_partman.tar.gz \
        --directory /usr/src/pg_partman \
        --strip-components 1 \
    # Delete src file tar
    && rm pg_partman.tar.gz
# Install the extension
RUN cd /usr/src/pg_partman && make install

# Delete the src files for pg_partman
RUN rm -rf /usr/src/pg_partman
# Delete the dependencies for downloading and building the extensions, we no longer need them
RUN apk del .fetch-deps .build-deps