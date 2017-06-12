FROM node

RUN mkdir /app
WORKDIR /app

COPY package.json /app
RUN npm install
RUN npm install forever -g

COPY . /app

EXPOSE 80

CMD ["forever", "start"]