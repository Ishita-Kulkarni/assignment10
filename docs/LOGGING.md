# Logging Documentation

## Overview
The FastAPI Calculator application includes comprehensive logging to track all operations, errors, and system events. Logging is implemented throughout the application to aid in debugging, monitoring, and auditing.

## Logging Architecture

### Components

1. **logger_config.py** - Centralized logging configuration
2. **Console Handler** - Outputs INFO and above to stdout
3. **File Handler** - Writes all logs (DEBUG and above) to `logs/app.log`
4. **Error Handler** - Writes ERROR logs to `logs/error.log`

### Log Levels

The application uses standard Python logging levels:
- **DEBUG**: Detailed information for diagnosing problems
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially problematic situations
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical errors that may cause application failure

## Log Files

### Location
All logs are stored in the `logs/` directory:
```
logs/
├── app.log      # All application logs (INFO, DEBUG, WARNING, ERROR)
└── error.log    # Error logs only (ERROR, CRITICAL)
```

### Log Rotation
- **Max File Size**: 10 MB per log file
- **Backup Count**: 5 backup files retained
- **Naming**: Rotated files are named `app.log.1`, `app.log.2`, etc.

## Log Format

### Console Output (Simple Format)
```
2025-11-06 19:00:00 - INFO - Application started successfully
```

### File Output (Detailed Format)
```
2025-11-06 19:00:00 - fastapi_calculator - INFO - main.py:50 - calculate_endpoint() - Calculation successful, returning result: 15.0
```

## What Gets Logged

### Application Lifecycle
- ✓ Application startup
- ✓ Application shutdown
- ✓ Logger initialization

### HTTP Requests (Middleware)
- ✓ Incoming request method and path
- ✓ Request headers (DEBUG level)
- ✓ Response status code
- ✓ Request duration
- ✓ Failed requests with error details

### API Endpoints

#### Root Endpoint (`/`)
- INFO: Endpoint access

#### Calculate Endpoint (`/calculate`)
- INFO: Request parameters (num1, num2, operation)
- INFO: Successful calculation result
- WARNING: Division by zero errors
- WARNING: Invalid operation errors
- ERROR: Unexpected errors

#### Health Endpoint (`/health`)
- DEBUG: Health check access

### Calculator Operations

#### All Operations (add, subtract, multiply, divide)
- DEBUG: Operation inputs
- DEBUG: Operation results
- ERROR: Division by zero (in divide function)
- ERROR: Invalid operations (in calculate function)

## Configuration

### Setup Logging
```python
from logger_config import setup_logging

# Initialize with default INFO level
logger = setup_logging()

# Or specify a different level
logger = setup_logging("DEBUG")
```

### Get Logger Instance
```python
from logger_config import get_logger

logger = get_logger()
logger.info("Your message here")
```

## Usage Examples

### Basic Logging
```python
from logger_config import get_logger

logger = get_logger()

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### Logging with Exception Information
```python
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
```

## Viewing Logs

### Real-time Console Output
When running the application, INFO and above messages are displayed in the console:
```bash
python main.py
```

### Viewing Log Files
```bash
# View all logs
cat logs/app.log

# View error logs only
cat logs/error.log

# Follow logs in real-time
tail -f logs/app.log

# Search logs
grep "ERROR" logs/app.log
grep "calculate" logs/app.log
```

## Log Analysis

### Common Log Patterns

#### Successful Calculation
```
INFO - Calculate endpoint called with: num1=10, num2=5, operation=add
INFO - Calculate called: num1=10, num2=5, operation=add
DEBUG - Addition: 10 + 5
DEBUG - Addition result: 15
INFO - Calculation successful: 10 add 5 = 15
INFO - Calculation successful, returning result: 15.0
```

#### Division by Zero
```
INFO - Calculate endpoint called with: num1=10, num2=0, operation=divide
INFO - Calculate called: num1=10, num2=0, operation=divide
DEBUG - Division: 10 / 0
ERROR - Division by zero attempted: 10 / 0
ERROR - Division by zero error: 10 / 0
WARNING - Division by zero error: Cannot divide by zero
```

#### Invalid Operation
```
INFO - Calculate endpoint called with: num1=10, num2=5, operation=power
INFO - Calculate called: num1=10, num2=5, operation=power
ERROR - Invalid operation requested: power
WARNING - Invalid operation error: Invalid operation: power
```

## Performance Monitoring

### Request Duration Tracking
Every HTTP request includes duration tracking:
```
INFO - Request completed: POST /calculate - Status: 200 - Duration: 0.003s
```

### Custom Header
The application adds a custom `X-Process-Time` header to all responses containing the processing time in seconds.

## Best Practices

### Do's
✓ Use appropriate log levels (DEBUG for detailed info, INFO for general events, ERROR for problems)
✓ Include relevant context in log messages (function parameters, return values)
✓ Log exceptions with `exc_info=True` for full stack traces
✓ Use structured log messages for easy parsing

### Don'ts
✗ Don't log sensitive information (passwords, API keys, personal data)
✗ Don't log in tight loops (can fill disk space quickly)
✗ Don't use print() statements - use the logger instead
✗ Don't log at ERROR level for expected exceptions

## Testing

Logging functionality is fully tested. Run logging tests:
```bash
pytest tests/test_logging.py -v
```

## Troubleshooting

### Logs Not Appearing
1. Check if `logs/` directory exists
2. Verify file permissions
3. Check log level configuration

### Disk Space Issues
1. Monitor log file sizes
2. Adjust rotation settings if needed
3. Consider external log aggregation

### Performance Impact
Logging has minimal performance impact:
- Async operations don't block
- File I/O is buffered
- Console output is non-blocking

## Production Recommendations

### For Production Environments:
1. Set log level to INFO or WARNING
2. Use external log aggregation (ELK, Splunk, CloudWatch)
3. Monitor log file sizes
4. Set up log rotation
5. Implement log retention policies
6. Consider structured logging (JSON format)

### Environment-based Configuration
```python
import os
log_level = os.getenv("LOG_LEVEL", "INFO")
logger = setup_logging(log_level)
```

## Integration with Monitoring Tools

### Log Aggregation
Logs can be integrated with:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Splunk**
- **AWS CloudWatch**
- **Google Cloud Logging**
- **Azure Monitor**

### Log Forwarding
Configure log forwarding in production:
```bash
# Example: Forward logs to syslog
logger.addHandler(SysLogHandler(address='/dev/log'))
```

## Summary

The logging system provides:
- ✓ Comprehensive tracking of all operations
- ✓ Multiple log levels for different scenarios
- ✓ Rotating file handlers to prevent disk space issues
- ✓ Both console and file output
- ✓ Performance monitoring with request duration
- ✓ Structured log messages for easy analysis
- ✓ Full test coverage
