# Frontend Dockerfile for Todo App
# Node 20-alpine with npm

FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Expose Next.js port
EXPOSE 3000

# Run Next.js dev server (command overridden in docker-compose.yml)
CMD ["npm", "run", "dev"]
