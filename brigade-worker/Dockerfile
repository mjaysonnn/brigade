FROM node:8-alpine
ARG network=host

WORKDIR /home/src
COPY brigade-worker/ /home/src/
#RUN npm install -g nedb
RUN npm install -g influx --save
RUN yarn build
CMD yarn run test
