FROM node:22-alpine
WORKDIR /worker
COPY package.json .
RUN npm install --omit=dev
COPY worker.js .
CMD ["npm", "start"]
