# Quick Reference Card

## 🚀 Essential Commands

### Local Development

```bash
# Start Docker containers
docker compose up --build

# Stop containers
docker compose down

# View logs
docker compose logs -f

# Access API docs
open http://localhost:8000/docs
```

### Testing

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_users.py -v

# Run user management tests only
pytest tests/test_auth.py tests/test_schemas.py tests/test_models.py tests/test_users.py -v
```

### Database

```bash
# Access pgAdmin
open http://localhost:5050
# Login: admin@example.com / admin

# Connect to PostgreSQL in pgAdmin
# Host: db (or postgres)
# Port: 5432
# Database: calculator_db
# Username: calculator_user
# Password: calculator_pass
```

### Docker

```bash
# Build Docker image
docker build -t fastapi-user-management:latest .

# Run Docker image
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  fastapi-user-management:latest

# Pull from Docker Hub
docker pull YOUR_USERNAME/fastapi-user-management:latest
```

### Git & CI/CD

```bash
# Push to trigger CI/CD (main branch only deploys)
git push origin main

# View workflow status
open https://github.com/YOUR_USERNAME/YOUR_REPO/actions

# View Docker Hub images
open https://hub.docker.com/r/YOUR_USERNAME/fastapi-user-management
```

---

## 📋 API Endpoints Quick Reference

### User Management

```bash
# Register user
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"password123"}'

# Login
curl -X POST "http://localhost:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"password123"}'

# Get all users
curl http://localhost:8000/users

# Get user by ID
curl http://localhost:8000/users/1

# Update user
curl -X PUT "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{"email":"newemail@example.com"}'

# Delete user
curl -X DELETE http://localhost:8000/users/1
```

### Calculator

```bash
# Calculate
curl -X POST "http://localhost:8000/calculate" \
  -H "Content-Type: application/json" \
  -d '{"num1":10,"num2":5,"operation":"add"}'

# Health check
curl http://localhost:8000/health
```

---

## 🔧 Troubleshooting Quick Fixes

### Tests Failing

```bash
# Ensure correct bcrypt version
pip install bcrypt==4.0.1

# Reinstall dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# Clear pytest cache
rm -rf .pytest_cache __pycache__
pytest -v
```

### Docker Issues

```bash
# Remove all containers and volumes
docker compose down -v

# Rebuild from scratch
docker compose build --no-cache
docker compose up

# Check container logs
docker compose logs web
docker compose logs db
```

### Database Issues

```bash
# Reset database
docker compose down -v
docker compose up --build

# Access PostgreSQL directly
docker exec -it fastapi-db-1 psql -U calculator_user -d calculator_db
```

### CI/CD Issues

```bash
# Verify secrets are set
# Go to: Settings > Secrets and variables > Actions
# Should see: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN

# Check workflow file syntax
cat .github/workflows/ci.yml | grep "DOCKERHUB"

# Test Docker build locally
docker build -t test .
```

---

## 📊 Test Coverage

| Component | Tests | Coverage |
|-----------|-------|----------|
| Password Hashing | 12 | 100% |
| Schemas | 20 | 100% |
| Models | 10 | 100% |
| User API | 18 | 93% |
| **Total** | **60** | **75%** |

---

## 🔐 Important Security Notes

⚠️ **Never commit**:
- `.env` file
- Passwords
- API keys
- Docker Hub credentials

✅ **Always use**:
- GitHub Secrets for CI/CD
- Access tokens (not passwords)
- bcrypt 4.0.1 (not 5.0.0)
- Environment variables

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `models.py` | User SQLAlchemy model |
| `schemas.py` | Pydantic validation |
| `auth.py` | Password hashing |
| `users.py` | User API endpoints |
| `database.py` | Database config |
| `main.py` | FastAPI app |
| `.github/workflows/ci.yml` | CI/CD pipeline |
| `.env.example` | Environment template |

---

## 🎯 Success Indicators

✅ All 60 tests passing  
✅ 75% code coverage  
✅ Docker containers running  
✅ CI/CD pipeline green  
✅ Docker image on Docker Hub  
✅ API accessible at localhost:8000  

---

## 📞 Quick Links

- **API Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050
- **GitHub Actions**: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
- **Docker Hub**: https://hub.docker.com/r/YOUR_USERNAME/fastapi-user-management

---

## 💡 Pro Tips

1. **Before pushing**: Run `pytest -v` locally
2. **First build**: Takes 5-10 min, later builds 2-3 min
3. **Main branch only**: Docker deployment only on main
4. **Coverage reports**: Open `htmlcov/index.html` after `pytest --cov`
5. **Debug CI/CD**: Check GitHub Actions logs first

---

## 🆘 Emergency Commands

```bash
# Complete reset
docker compose down -v
rm -rf __pycache__ .pytest_cache htmlcov .coverage
pip install -r requirements.txt -r requirements-test.txt
pytest -v
docker compose up --build

# Quick test
pytest tests/test_users.py -v -k "test_register_user"

# Quick Docker test
docker build -t test . && docker run -p 8000:8000 test
```

---

**For detailed information, see:**
- `README.md` - Complete documentation
- `CI_CD_SETUP.md` - CI/CD setup guide
- `SETUP_CHECKLIST.md` - Setup checklist
- `ASSIGNMENT_SUMMARY.md` - Assignment summary
