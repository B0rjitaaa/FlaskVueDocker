FROM node:8

COPY ./frontend /frontend

WORKDIR /frontend

# Borra esas lineas
# RUN npm --user root --unsafe-perm true install npm -g

RUN npm install -g --silent \
	yarn \
	vue-cli

EXPOSE 8080

CMD ["npm", "run", "dev"]

