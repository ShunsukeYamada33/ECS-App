FROM node:20

WORKDIR /frontend

COPY package*.json ./

# 追加：npm を最新にしておく
RUN npm install -g npm@latest

RUN npm install

COPY . .

CMD ["npm", "run", "dev"]
