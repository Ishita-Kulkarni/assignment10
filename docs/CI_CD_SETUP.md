# CI/CD Setup Guide

This guide will help you set up the complete CI/CD pipeline for automated testing and Docker Hub deployment.

## Prerequisites

- GitHub account
- Docker Hub account
- Repository pushed to GitHub
- Docker installed locally (for testing)

## Step-by-Step Setup

### 1. Create Docker Hub Repository

1. Log in to [Docker Hub](https://hub.docker.com/)
2. Click "Create Repository"
3. Name it: `fastapi-user-management`
4. Set visibility (Public or Private)
5. Click "Create"

### 2. Generate Docker Hub Access Token

🔐 **Important**: Use an access token, NOT your Docker Hub password!

1. Go to Docker Hub → Account Settings → Security
2. Click "New Access Token"
3. Name: `GitHub Actions CI/CD`
4. Permissions: Read & Write
5. Click "Generate"
6. **Copy the token immediately** (you won't see it again!)

### 3. Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to: `Settings > Secrets and variables > Actions`
3. Click "New repository secret"

Add these two secrets:

**Secret 1: DOCKERHUB_USERNAME**
- Name: `DOCKERHUB_USERNAME`
- Value: Your Docker Hub username (e.g., `johndoe`)

**Secret 2: DOCKERHUB_TOKEN**
- Name: `DOCKERHUB_TOKEN`
- Value: The access token you copied in step 2

### 4. Update Workflow Configuration

Edit `.github/workflows/ci.yml`:

Find this line (around line 165):
```yaml
images: ${{ secrets.DOCKERHUB_USERNAME }}/fastapi-user-management
```

This is already configured to use your Docker Hub username from secrets!

Also update lines 173-174 if needed:
```yaml
cache-from: type=registry,ref=${{ secrets.DOCKERHUB_USERNAME }}/fastapi-user-management:buildcache
cache-to: type=registry,ref=${{ secrets.DOCKERHUB_USERNAME }}/fastapi-user-management:buildcache,mode=max
```

### 5. Update README Badges

Edit `README.md` and replace:
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO` with your repository name
- Update Docker Hub image references

### 6. Test Locally (Optional but Recommended)

Before pushing, test the Docker build:

```bash
# Build the image
docker build -t fastapi-user-management:test .

# Run tests
pytest -v --cov=.

# Test the Docker image
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@localhost:5432/db \
  fastapi-user-management:test
```

### 7. Push to GitHub

Commit and push your changes:

```bash
git add .
git commit -m "Configure CI/CD pipeline"
git push origin main
```

### 8. Monitor the Pipeline

1. Go to your GitHub repository
2. Click the "Actions" tab
3. You should see the workflow running
4. Click on the workflow run to see details

**Expected Timeline:**
- Testing phase: 3-5 minutes
- Build & push phase: 5-10 minutes (first time)
- Total: 8-15 minutes

### 9. Verify Docker Hub

After the workflow completes:

1. Go to Docker Hub
2. Open your `fastapi-user-management` repository
3. Check the "Tags" tab
4. You should see:
   - `latest`
   - `main`
   - `main-<commit-sha>`

### 10. Test the Deployed Image

Pull and run your image from Docker Hub:

```bash
# Pull the image
docker pull YOUR_USERNAME/fastapi-user-management:latest

# Run it
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/calculator_db \
  YOUR_USERNAME/fastapi-user-management:latest

# Test the API
curl http://localhost:8000/health
```

## Pipeline Behavior

### What Triggers the Pipeline?

| Event | Test Job | Build Job | Push to Docker Hub |
|-------|----------|-----------|-------------------|
| Push to `main` | ✅ | ✅ | ✅ |
| Push to `develop` | ✅ | ❌ | ❌ |
| Pull request to `main` | ✅ | ❌ | ❌ |
| Pull request to `develop` | ✅ | ❌ | ❌ |

### What Gets Tested?

✅ Python 3.9, 3.10, 3.11, 3.12 compatibility  
✅ Code linting with flake8  
✅ 12 password hashing tests  
✅ 20 Pydantic schema tests  
✅ 10 SQLAlchemy model tests  
✅ 18 user API integration tests  
✅ 37 calculator operation tests  
✅ 37 calculator API tests  
✅ 26 logging tests  
✅ Code coverage reporting  

**Total: 160 tests across all Python versions**

### What Gets Built?

When tests pass on `main` branch:
1. Multi-stage Docker image
2. Optimized with layer caching
3. Tagged with:
   - `latest`
   - `main`
   - `main-<commit-sha>`
4. Pushed to Docker Hub

## Troubleshooting

### Problem: Workflow fails on "Log in to Docker Hub"

**Error**: `Error: Invalid username/password`

**Solution**:
- Verify `DOCKERHUB_USERNAME` is your exact username
- Verify `DOCKERHUB_TOKEN` is an access token (not password)
- Check token hasn't expired
- Regenerate token if needed

### Problem: Tests pass locally but fail in CI

**Possible causes**:
1. Python version differences
2. Missing dependencies in `requirements-test.txt`
3. Database connection issues

**Solution**:
```bash
# Test with specific Python version
python3.9 -m pytest -v

# Check requirements
pip freeze > current-deps.txt
diff requirements.txt current-deps.txt
```

### Problem: Docker build fails

**Error**: `failed to solve with frontend dockerfile.v0`

**Solution**:
- Check Dockerfile syntax
- Ensure `requirements.txt` exists
- Verify all COPY paths are correct

### Problem: Build takes too long

**Normal behavior**:
- First build: 5-10 minutes
- Subsequent builds: 2-3 minutes (with cache)

**If always slow**:
- Check build cache configuration
- Ensure Buildx is set up correctly
- Verify cache repository permissions

### Problem: Tests pass but Docker push skipped

**Reason**: Build job only runs on `main` branch pushes

**Solution**:
```bash
# Check your current branch
git branch

# If on develop, merge to main
git checkout main
git merge develop
git push origin main
```

## Security Checklist

✅ Never commit `.env` file  
✅ Never commit Docker Hub credentials  
✅ Use GitHub Secrets for sensitive data  
✅ Use access tokens, not passwords  
✅ Rotate tokens periodically  
✅ Set minimum required permissions  
✅ Review workflow logs for exposed secrets  

## Advanced Configuration

### Change Image Name

Edit `.github/workflows/ci.yml`:
```yaml
images: ${{ secrets.DOCKERHUB_USERNAME }}/NEW_NAME_HERE
```

### Add More Python Versions

Edit `.github/workflows/ci.yml`:
```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11', '3.12', '3.13']
```

### Deploy to Production After Tests

Add to `.github/workflows/ci.yml`:
```yaml
deploy:
  runs-on: ubuntu-latest
  needs: build-and-push
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  
  steps:
    - name: Deploy to production
      run: |
        # Add your deployment commands here
        echo "Deploying to production..."
```

### Enable Manual Workflow Trigger

Add to `.github/workflows/ci.yml` (top of file):
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  workflow_dispatch:  # Enables manual trigger
```

## Monitoring and Maintenance

### Check CI/CD Status

- **GitHub Actions**: See all workflow runs
- **Docker Hub**: Verify images are pushed
- **Codecov**: Review coverage reports

### Regular Maintenance

Weekly:
- Review failed workflows
- Check coverage trends
- Update dependencies

Monthly:
- Rotate access tokens
- Review security alerts
- Update GitHub Actions versions

Quarterly:
- Audit secrets and permissions
- Review and optimize build times
- Update Docker base images

## Success Indicators

✅ Green checkmark on commits  
✅ All tests passing (60+ tests)  
✅ Coverage reports uploaded to Codecov  
✅ Docker images on Docker Hub with tags  
✅ Build time under 3 minutes (after first build)  
✅ No secrets exposed in logs  

## Next Steps

After successful CI/CD setup:

1. **Enable Branch Protection**
   - Go to Settings → Branches
   - Add rule for `main` branch
   - Require status checks to pass
   - Require pull request reviews

2. **Set Up Codecov** (optional)
   - Sign up at codecov.io
   - Connect your repository
   - Add `CODECOV_TOKEN` to GitHub Secrets

3. **Add Status Badges**
   - Get badge URLs from GitHub Actions
   - Add to README.md

4. **Configure Notifications**
   - Settings → Notifications
   - Enable email or Slack notifications
   - Get alerts for failed builds

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [GitHub Secrets Best Practices](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review GitHub Actions logs
3. Check Docker Hub build logs
4. Open an issue with:
   - Error message
   - Workflow run link
   - Steps to reproduce
