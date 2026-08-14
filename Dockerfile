FROM lscr.io/linuxserver/chromium:latest

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

COPY tools/browser-publisher/cdp-proxy.sh /custom-services.d/cdp-proxy
RUN chmod 0755 /custom-services.d/cdp-proxy
