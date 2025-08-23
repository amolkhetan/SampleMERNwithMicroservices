# Use official Node.js LTS image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .
npm install

# Expose port (adjust if needed)
EXPOSE 3000

# Start the frontend server
CMD ["npm", "start"]