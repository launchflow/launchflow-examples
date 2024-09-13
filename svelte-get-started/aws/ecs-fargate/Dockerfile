FROM public.ecr.aws/docker/library/node:18-alpine AS base

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

ENV NODE_ENV=production

RUN npm prune --production

FROM public.ecr.aws/docker/library/node:18-alpine

WORKDIR /app

COPY --from=base /app/build build/
COPY --from=base /app/node_modules node_modules/
COPY package.json .

ENV PORT=80
EXPOSE $PORT
CMD ["node", "build"]
