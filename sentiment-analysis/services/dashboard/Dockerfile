FROM node:18-alpine

WORKDIR /app

# Install dependencies first (cached layer)
COPY package.json .
RUN npm install

# Copy app files
COPY . .

CMD ["npm", "start"]
