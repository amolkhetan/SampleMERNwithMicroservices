# Use official Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./

RUN npm install

# Copy the rest of the frontend source code
COPY . .

# Expose the development server port
EXPOSE 3005

# Start the frontend in development mode
CMD ["npm", "start"]
