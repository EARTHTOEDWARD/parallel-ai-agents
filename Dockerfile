# ---------- stage 1: build ----------
FROM node:18-bookworm AS builder
WORKDIR /app
COPY package*.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build

# ---------- stage 2: runtime ----------
FROM node:18-slim
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app .
EXPOSE 3000
CMD ["pnpm","run","start"]