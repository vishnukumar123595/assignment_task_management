# Use official Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy app code
COPY . .

# Expose Next.js default port
EXPOSE 3000

# Start the Next.js app
CMD ["npm", "run", "dev"]
