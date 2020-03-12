FROM node:10-slim

RUN npm i npm@latest -g

RUN mkdir -p /src/{client,server}
WORKDIR /src

COPY package.json package-lock.json* ./
COPY client/package.json client/package-lock.json* ./client/
COPY server/package.json server/package-lock.json* ./server/
RUN npm run init

COPY . .

CMD ["npm", "start"]