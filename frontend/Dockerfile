# Use a lightweight Nginx image
FROM nginx:alpine

# Copy the static files to the Nginx html directory
COPY index.html /usr/share/nginx/html/index.html

# Copy custom nginx config for backend proxying
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Nginx starts automatically
