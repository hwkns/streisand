# Dockerfile for development

FROM node:8.11

WORKDIR /code

COPY package*.json .
RUN npm install
ENV PATH="$(npm bin):$PATH"
EXPOSE 3000
CMD ["gulp" "dev"]
