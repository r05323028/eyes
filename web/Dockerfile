FROM node:lts-buster

COPY . /app
RUN npm install -g serve

WORKDIR /app
RUN npm ci
RUN npm run build