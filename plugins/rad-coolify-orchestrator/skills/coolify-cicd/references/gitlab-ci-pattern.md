# GitLab CI Integration with Coolify

## Direct API Trigger (Simplest)

### .gitlab-ci.yml

```yaml
stages:
  - test
  - deploy

test:
  stage: test
  image: node:20-alpine
  script:
    - npm ci
    - npm test

deploy-staging:
  stage: deploy
  image: curlimages/curl:latest
  only:
    - develop
  script:
    - |
      curl -X POST \
        "${COOLIFY_URL}/api/v1/applications/${COOLIFY_STAGING_UUID}/deploy" \
        -H "Authorization: Bearer ${COOLIFY_API_TOKEN}" \
        -H "Content-Type: application/json" \
        --fail --silent --show-error

deploy-production:
  stage: deploy
  image: curlimages/curl:latest
  only:
    - main
  when: manual    # Require manual approval for production
  script:
    - |
      curl -X POST \
        "${COOLIFY_URL}/api/v1/applications/${COOLIFY_PROD_UUID}/deploy" \
        -H "Authorization: Bearer ${COOLIFY_API_TOKEN}" \
        -H "Content-Type: application/json" \
        --fail --silent --show-error
```

### Required GitLab CI/CD Variables

Set in **Settings → CI/CD → Variables**:

| Variable | Value | Protected | Masked |
|----------|-------|-----------|--------|
| `COOLIFY_URL` | `https://coolify.example.com` | Yes | No |
| `COOLIFY_API_TOKEN` | API token from Coolify | Yes | Yes |
| `COOLIFY_STAGING_UUID` | Staging app UUID | Yes | No |
| `COOLIFY_PROD_UUID` | Production app UUID | Yes | Yes |

## GHCR-Equivalent with GitLab Container Registry

```yaml
stages:
  - build
  - deploy

variables:
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG

deploy:
  stage: deploy
  image: curlimages/curl:latest
  only:
    - main
  script:
    # Update image tag
    - |
      curl -X PATCH \
        "${COOLIFY_URL}/api/v1/applications/${COOLIFY_APP_UUID}" \
        -H "Authorization: Bearer ${COOLIFY_API_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{\"docker_registry_image_tag\": \"${CI_COMMIT_SHA}\"}" \
        --fail
    # Trigger deploy
    - |
      curl -X POST \
        "${COOLIFY_URL}/api/v1/applications/${COOLIFY_APP_UUID}/deploy" \
        -H "Authorization: Bearer ${COOLIFY_API_TOKEN}" \
        --fail
```

### Coolify Configuration for GitLab Registry

1. Add Docker Registry in Coolify: **Settings → Docker Registries**
   - Registry URL: `registry.gitlab.com`
   - Username: A GitLab deploy token or personal access token username
   - Password: The deploy token or PAT with `read_registry` scope
2. Create application with **Docker Image** build pack
3. Set image to `registry.gitlab.com/<GROUP>/<PROJECT>:latest`

## Deploy and Wait Pattern

```yaml
deploy-with-status:
  stage: deploy
  image: curlimages/curl:latest
  script:
    - |
      # Trigger deploy and capture response
      RESPONSE=$(curl -s -X POST \
        "${COOLIFY_URL}/api/v1/applications/${COOLIFY_APP_UUID}/deploy" \
        -H "Authorization: Bearer ${COOLIFY_API_TOKEN}" \
        -H "Content-Type: application/json")
      
      DEPLOY_UUID=$(echo "$RESPONSE" | grep -o '"deployment_uuid":"[^"]*"' | cut -d'"' -f4)
      echo "Deployment started: $DEPLOY_UUID"
      
      # Poll for completion
      for i in $(seq 1 20); do
        sleep 15
        STATUS=$(curl -s \
          "${COOLIFY_URL}/api/v1/applications/${COOLIFY_APP_UUID}/deployments/${DEPLOY_UUID}" \
          -H "Authorization: Bearer ${COOLIFY_API_TOKEN}" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)
        
        echo "Attempt $i: $STATUS"
        
        if [ "$STATUS" = "finished" ]; then
          echo "Deploy succeeded!"
          exit 0
        elif [ "$STATUS" = "failed" ] || [ "$STATUS" = "cancelled" ]; then
          echo "Deploy failed: $STATUS"
          exit 1
        fi
      done
      
      echo "Deploy timed out after 5 minutes"
      exit 1
```

## Webhook Alternative (No API Token Needed)

```yaml
deploy-webhook:
  stage: deploy
  image: curlimages/curl:latest
  only:
    - main
  script:
    - curl -X POST "${COOLIFY_WEBHOOK_URL}" --fail --silent --show-error
```

Set `COOLIFY_WEBHOOK_URL` as a CI/CD variable containing the full webhook URL from Coolify's application settings.
