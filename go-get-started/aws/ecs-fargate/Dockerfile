FROM public.ecr.aws/docker/library/golang:1.20 as builder

WORKDIR /app
COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o /go/bin/app

FROM public.ecr.aws/docker/library/alpine:3.14

COPY --from=builder /go/bin/app /go/bin/app

ENV HOST=0.0.0.0
ENV PORT=80

ENTRYPOINT ["/go/bin/app"]
