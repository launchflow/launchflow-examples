FROM public.ecr.aws/docker/library/openjdk:17-jdk-slim as build
WORKDIR /workspace/app

COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
COPY src src

RUN ./mvnw install -DskipTests
RUN mkdir -p target/dependency && (cd target/dependency; jar -xf ../*.jar)

FROM public.ecr.aws/docker/library/openjdk:17-jdk-slim
WORKDIR /app
VOLUME /tmp
ARG DEPENDENCY=/workspace/app/target/dependency
COPY --from=build ${DEPENDENCY}/BOOT-INF/lib /app/lib
COPY --from=build ${DEPENDENCY}/META-INF /app/META-INF
COPY --from=build ${DEPENDENCY}/BOOT-INF/classes /app

ENV PORT=80
EXPOSE $PORT
ENTRYPOINT ["java","-cp","app:app/lib/*","com.example.demo.DemoApplication"]
