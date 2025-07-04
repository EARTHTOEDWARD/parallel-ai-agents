# Test Agent Mission Brief

## Role & Ownership

**Agent ID**: test-opus  
**Branch**: test-opus  
**Owned Paths**:

- `/tests/**/*`
- Test documentation in `/docs/testing/`
- Test fixtures and mocks
- Performance benchmarks

**Forbidden Paths**:

- `/backend/**/*` (owned by backend-opus)
- `/frontend/**/*` (owned by frontend-opus)
- Production configuration files

## External Contracts

### Test Structure

```javascript
// Unit Test Pattern
describe('ComponentName', () => {
  describe('methodName', () => {
    it('should handle expected behavior', () => {
      // Arrange
      // Act
      // Assert
    });

    it('should handle error cases', () => {
      // Test error scenarios
    });
  });
});

// Integration Test Pattern
describe('API: /endpoint', () => {
  beforeEach(() => {
    // Setup test database
    // Clear cache
  });

  afterEach(() => {
    // Cleanup
  });

  it('should return 200 with valid data', async () => {
    // Test happy path
  });
});
```

### Test Data Management

```json
{
  "testUsers": [
    {
      "id": "test-user-1",
      "email": "test1@example.com",
      "role": "admin"
    }
  ],
  "testApiKeys": {
    "valid": "test-api-key-valid",
    "expired": "test-api-key-expired",
    "invalid": "test-api-key-invalid"
  }
}
```

## Definition of Done

✅ **Unit test coverage ≥ 80%**  
✅ **Integration tests for all API endpoints**  
✅ **E2E tests for critical user flows**  
✅ **Performance tests establish baselines**  
✅ **Security tests for auth flows**  
✅ **Accessibility tests pass**  
✅ **Test documentation updated**  
✅ **No flaky tests** (run 3x successfully)  
✅ **CI test suite completes < 5 minutes**  
✅ **Test reports generated**

## Interface with Siblings

### From Backend Agent

Require from backend:

1. API client examples
2. Test database seeds
3. Authentication test tokens
4. Rate limit configurations

### From Frontend Agent

Require from frontend:

1. Component test IDs
2. Page object models
3. Critical user journeys
4. Performance budgets

### Provide to Siblings

1. Test results dashboard
2. Coverage reports
3. Performance benchmarks
4. Failing test details with reproduction steps

## Git Commit Format

All commits must follow this format:

```
[test-opus] <type>: <description>

<optional body>

<optional footer>
```

Types:

- `test`: New tests added
- `fix`: Fix flaky/broken tests
- `refactor`: Improve test structure
- `perf`: Optimize test performance
- `docs`: Update test documentation
- `ci`: Update test pipeline

Examples:

```
[test-opus] test: add integration tests for user auth
[test-opus] fix: stabilize flaky navigation test
[test-opus] perf: parallelize API test suite
```

## Additional Guidelines

### Test Categories

1. **Unit Tests**:
   - Test individual functions/methods
   - Mock external dependencies
   - Fast execution (< 100ms per test)
   - Located near source files

2. **Integration Tests**:
   - Test module interactions
   - Use test database
   - Test API contracts
   - Located in `/tests/integration/`

3. **E2E Tests**:
   - Test complete user flows
   - Run against staging environment
   - Cover critical paths only
   - Located in `/tests/e2e/`

4. **Performance Tests**:
   - Establish baselines
   - Monitor regressions
   - Test under load
   - Located in `/tests/performance/`

### Test Writing Rules

1. **Descriptive Names**:

   ```javascript
   // Good
   it('should return 401 when auth token is expired');

   // Bad
   it('test auth');
   ```

2. **Isolated Tests**:
   - No dependencies between tests
   - Clean state before each test
   - Use factories for test data

3. **Deterministic**:
   - No random values without seeds
   - Mock time-dependent operations
   - Control external dependencies

4. **Maintainable**:
   - DRY principle for test utilities
   - Clear arrange-act-assert structure
   - Helpful error messages

### Quality Metrics

Track and report:

- Code coverage by module
- Test execution time
- Flaky test frequency
- Bug escape rate
- Time to fix failing tests

### Continuous Improvement

1. Review failing tests weekly
2. Refactor slow tests
3. Add tests for bug fixes
4. Update tests with API changes
5. Document testing patterns
