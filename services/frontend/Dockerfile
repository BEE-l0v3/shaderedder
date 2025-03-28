FROM node:21-alpine3.19

WORKDIR /app 

COPY yarn.lock package.json ./

RUN yarn config set ignore-engines true
RUN yarn install

COPY . . 

EXPOSE 8080

