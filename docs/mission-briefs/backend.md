# Backend Agent Mission Brief

## Role & Ownership

**Agent ID**: backend-opus  
**Branch**: backend-opus  
**Owned Paths**:

- `/backend/**/*`
- Database migrations
- API documentation in `/docs/api/`

**Forbidden Paths**:

- `/frontend/**/*` (owned by frontend-opus)
- `/tests/**/*` (owned by test-opus)
- CI/CD configuration files

## External Contracts

### API Endpoints

All endpoints must return JSON matching these schemas:

```json
// Success Response
{
  "success": true,
  "data": <resource>,
  "meta": {
    "timestamp": "ISO-8601",
    "version": "1.0.0"
  }
}

// Error Response
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  }
}
```

### Required Endpoints (Phase 1)

- `GET /api/health` - Health check
- `POST /api/auth/login` - User authentication
- `GET /api/auth/logout` - Session termination
- CRUD operations for primary resources

### Database Schema

- Use migrations for all schema changes
- Follow naming convention: `YYYYMMDD_HHMMSS_description.sql`
- Document foreign key relationships

## Definition of Done

✅ **All unit tests pass** (`npm test` or `pytest`)  
✅ **Integration tests for API endpoints pass**  
✅ **API documentation updated** (OpenAPI/Swagger)  
✅ **No linting errors** (`eslint` or `ruff`)  
✅ **Type checking passes** (`tsc` or `mypy`)  
✅ **Database migrations tested** (up and down)  
✅ **Error handling for all edge cases**  
✅ **Request validation implemented**  
✅ **Authentication/authorization working**  
✅ **CI pipeline green**

## Interface with Siblings

### Frontend Requirements

Before frontend can integrate:

1. API endpoints must be documented in OpenAPI format
2. CORS configuration must allow frontend origin
3. Authentication tokens must use standard JWT format
4. Error responses must follow the contract schema

### Test Agent Dependencies

1. Provide API client SDK or examples
2. Document test user credentials
3. Ensure test database can be reset
4. Provide performance benchmarks

## Git Commit Format

All commits must follow this format:

```
[backend-opus] <type>: <description>

<optional body>

<optional footer>
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, semicolons, etc)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:

```
[backend-opus] feat: implement user authentication endpoint
[backend-opus] fix: handle null values in user profile update
[backend-opus] docs: add API examples for auth endpoints
```

## Additional Guidelines

1. **Security First**:
   - Never log sensitive data (passwords, tokens)
   - Validate all inputs
   - Use prepared statements for SQL
   - Implement rate limiting

2. **Performance**:
   - Use database indexes appropriately
   - Implement caching where beneficial
   - Monitor query performance
   - Use pagination for list endpoints

3. **Error Handling**:
   - Log errors with context
   - Return user-friendly error messages
   - Use appropriate HTTP status codes
   - Implement retry logic for external services

4. **Dependencies**:
   - Verify packages exist before adding
   - Check for security vulnerabilities
   - Document why each dependency is needed
   - Prefer well-maintained packages
