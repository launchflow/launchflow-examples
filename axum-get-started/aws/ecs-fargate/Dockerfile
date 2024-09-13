FROM public.ecr.aws/docker/library/rust:1.71 as builder

WORKDIR /app
COPY . .

RUN cargo build --release --bin launchflow-axum

FROM public.ecr.aws/docker/library/debian:bullseye AS runtime

WORKDIR /app
COPY --from=builder /app/target/release/launchflow-axum /usr/local/bin

ENV HOST=0.0.0.0
ENV PORT=80

ENTRYPOINT ["/usr/local/bin/launchflow-axum"]
