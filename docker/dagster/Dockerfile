# Dockerfile_user_code

FROM python:3.10-slim

RUN pip install \
    dagster \
    dagster-postgres \
    dagster-docker \
    dagster_dbt \
    dbt-postgres

# Add repository code
WORKDIR /opt/dagster/app

# COPY repo.py /opt/dagster/app

# Run dagster gRPC server on port 4000
EXPOSE 4000

# CMD allows this to be overridden from run launchers or executors that want
# to run other commands against your repository
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "repo.py"]
