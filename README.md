# Jenkins Demo App

A small dummy application used to demonstrate a Jenkins CI pipeline for the YT-setup project.

## CI flow

1. Open or update a pull request.
2. Jenkins runs the PR validation pipeline.
3. The pipeline runs unit tests, lint checks, and a Docker image build.
4. The PR is merged only after the required Jenkins checks pass.
5. A merge to `master` runs the release pipeline.
6. Jenkins creates a Git tag such as `v1.0.1`.
7. Jenkins builds the Docker image with the same tag.
8. Jenkins pushes the image to JFrog Artifactory.

The resulting image is the artifact that will be consumed by the CD pipeline later.

## Application

The application exposes:

- `/` - application information
- `/health` - health check

## Jenkins credentials expected

Configure these credential IDs in Jenkins before running the release stage:

- `github-token` - GitHub token with permission to create repository tags
- `artifactory-creds` - username/password for the JFrog Docker registry

Set the Artifactory Docker registry as the Jenkins environment variable `JFROG_REGISTRY`, for example:

```text
mycompany.jfrog.io/docker-local
```
