# Step 1: Build the app
FROM node:23.6 as build

# Set the working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the source code into the container
COPY . .

# Build the React app
RUN npm run build

# Step 2: Serve the app using a web server (e.g., nginx)
FROM nginx:alpine

# Copy the built React app from the build container
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for the React app
EXPOSE 80
