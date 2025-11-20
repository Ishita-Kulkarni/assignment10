# Quick Setup Checklist

Use this checklist to ensure complete setup of the FastAPI User Management System with CI/CD.

## Initial Setup

- [ ] Clone repository
- [ ] Copy `.env.example` to `.env`
- [ ] Update `.env` with your database credentials
- [ ] Install Docker Desktop
- [ ] Verify Docker is running: `docker --version`

## Local Development

- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Install test dependencies: `pip install -r requirements-test.txt`
- [ ] Run tests locally: `pytest -v --cov=.`
- [ ] Verify all 60 tests pass
- [ ] Check coverage is ≥ 75%

## Docker Setup

- [ ] Build containers: `docker compose up --build`
- [ ] Verify FastAPI is running: http://localhost:8000/docs
- [ ] Verify pgAdmin is accessible: http://localhost:5050
- [ ] Test database connection in pgAdmin
- [ ] Test API endpoints via Swagger UI

## Database Verification

- [ ] Log in to pgAdmin (admin@example.com / admin)
- [ ] Connect to database (host: db, port: 5432)
- [ ] Verify `users` table exists
- [ ] Test user registration via API
- [ ] Verify user appears in database

## Testing Verification

### Unit Tests
- [ ] `pytest tests/test_auth.py -v` (12 tests)
- [ ] `pytest tests/test_schemas.py -v` (20 tests)
- [ ] `pytest tests/test_models.py -v` (10 tests)

### Integration Tests
- [ ] `pytest tests/test_users.py -v` (18 tests)
- [ ] `pytest tests/test_operations.py -v` (37 tests)
- [ ] `pytest tests/test_main.py -v` (37 tests)

### All Tests
- [ ] `pytest -v` (all tests pass)
- [ ] `pytest --cov=. --cov-report=html` (generate coverage report)
- [ ] Open `htmlcov/index.html` to view coverage

## Docker Hub Setup

- [ ] Create Docker Hub account
- [ ] Create repository: `fastapi-user-management`
- [ ] Generate access token (Account Settings > Security)
- [ ] Save token securely (you won't see it again!)

## GitHub Setup

- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Verify `.github/workflows/ci.yml` exists

## GitHub Secrets Configuration

- [ ] Go to Settings > Secrets and variables > Actions
- [ ] Add secret: `DOCKERHUB_USERNAME` = your Docker Hub username
- [ ] Add secret: `DOCKERHUB_TOKEN` = your Docker Hub access token
- [ ] Verify secrets are saved (padlock icons)

## Workflow Configuration

- [ ] Open `.github/workflows/ci.yml`
- [ ] Verify image name: `${{ secrets.DOCKERHUB_USERNAME }}/fastapi-user-management`
- [ ] Verify cache references match your username
- [ ] Commit any changes

## CI/CD Testing

- [ ] Push to `main` branch: `git push origin main`
- [ ] Go to GitHub Actions tab
- [ ] Verify workflow starts running
- [ ] Wait for test job to complete (3-5 min)
- [ ] Verify all tests pass ✅
- [ ] Verify build-and-push job starts (main branch only)
- [ ] Wait for Docker build to complete (5-10 min first time)
- [ ] Verify workflow completes successfully ✅

## Docker Hub Verification

- [ ] Go to Docker Hub
- [ ] Open `fastapi-user-management` repository
- [ ] Check Tags tab
- [ ] Verify `latest` tag exists
- [ ] Verify `main` tag exists
- [ ] Verify `main-<commit-sha>` tag exists
- [ ] Check image size (should be < 500MB)

## Production Deployment Test

- [ ] Pull image: `docker pull YOUR_USERNAME/fastapi-user-management:latest`
- [ ] Run container:
  ```bash
  docker run -p 8000:8000 \
    -e DATABASE_URL=postgresql://user:pass@host:5432/db \
    YOUR_USERNAME/fastapi-user-management:latest
  ```
- [ ] Test health endpoint: `curl http://localhost:8000/health`
- [ ] Test API documentation: http://localhost:8000/docs
- [ ] Test user registration via API
- [ ] Stop container: `docker stop <container-id>`

## README Updates

- [ ] Replace `YOUR_USERNAME` with your GitHub username
- [ ] Replace `YOUR_REPO` with your repository name
- [ ] Update Docker Hub image references
- [ ] Add actual CI/CD badge URLs
- [ ] Commit changes: `git commit -m "Update README with actual usernames"`

## Branch Protection (Recommended)

- [ ] Go to Settings > Branches
- [ ] Add rule for `main` branch
- [ ] Enable "Require status checks to pass before merging"
- [ ] Select "test" as required check
- [ ] Enable "Require pull request reviews before merging"
- [ ] Save changes

## Optional: Codecov Integration

- [ ] Sign up at codecov.io
- [ ] Connect GitHub repository
- [ ] Copy Codecov token
- [ ] Add `CODECOV_TOKEN` to GitHub Secrets
- [ ] Update README with Codecov badge

## Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] No passwords in repository
- [ ] Docker Hub token is a secret (not password)
- [ ] GitHub Secrets are encrypted
- [ ] bcrypt version is 4.0.1 (not 5.0.0)
- [ ] Database passwords are strong
- [ ] All tests passing before deployment

## Documentation Verification

- [ ] README.md is comprehensive
- [ ] CI_CD_SETUP.md explains setup process
- [ ] .env.example documents all variables
- [ ] Code includes docstrings
- [ ] API documentation is accessible

## Final Verification

- [ ] All 60 tests passing locally
- [ ] All 60 tests passing in CI (x4 Python versions = 240 tests)
- [ ] Docker image builds successfully
- [ ] Docker image pushes to Docker Hub
- [ ] Image can be pulled and run
- [ ] API is accessible in production
- [ ] Database connections work
- [ ] No secrets in logs or repository

## Common Issues

### Tests fail with bcrypt error
**Solution**: Ensure bcrypt==4.0.1 in both `requirements.txt` and `requirements-test.txt`

### Docker login fails in CI
**Solution**: Verify DOCKERHUB_TOKEN is an access token, not your password

### Build not triggered
**Solution**: Ensure you pushed to `main` branch (build only runs on main)

### PostgreSQL connection fails
**Solution**: Check DATABASE_URL format: `postgresql://user:pass@host:port/db`

### Tests pass locally but fail in CI
**Solution**: Test with specific Python version: `python3.9 -m pytest -v`

## Success Criteria

✅ Local environment running  
✅ All tests passing (60/60)  
✅ Docker containers working  
✅ CI/CD pipeline configured  
✅ Tests passing in GitHub Actions  
✅ Docker image on Docker Hub  
✅ Documentation complete  
✅ Secrets properly configured  
✅ No security issues  
✅ Production deployment tested  

## Next Steps After Setup

1. Add more user features (password reset, email verification)
2. Implement JWT authentication
3. Add user roles and permissions
4. Set up monitoring and alerting
5. Configure automatic deployments
6. Add API rate limiting
7. Implement caching
8. Add more comprehensive logging

## Time Estimates

- Initial setup: 30 minutes
- Docker configuration: 15 minutes
- Testing verification: 20 minutes
- CI/CD setup: 30 minutes
- First deployment: 15 minutes
- Documentation: 20 minutes
- **Total: ~2 hours**

## Resources

- [CI_CD_SETUP.md](CI_CD_SETUP.md) - Detailed CI/CD guide
- [README.md](README.md) - Complete documentation
- [.env.example](.env.example) - Environment variables template
- [GitHub Actions](https://github.com/YOUR_USERNAME/YOUR_REPO/actions) - Pipeline status
- [Docker Hub](https://hub.docker.com/r/YOUR_USERNAME/fastapi-user-management) - Published images

---

**Need Help?**
- Review CI_CD_SETUP.md for detailed troubleshooting
- Check GitHub Actions logs for errors
- Verify all secrets are configured correctly
- Ensure Docker is running
- Test locally before pushing to GitHub
