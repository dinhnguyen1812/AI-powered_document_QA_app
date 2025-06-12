FROM node:18-alpine

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
RUN npm ci
RUN npm install axios @types/axios

COPY . .
RUN npm run build

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]

