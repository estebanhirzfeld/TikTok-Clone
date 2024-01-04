FROM nginx:1.23.3-alpine

# Remove default configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy Custom Configuration
COPY nginx.conf /etc/nginx/nginx.conf
