# Frontend Agent Mission Brief

## Role & Ownership

**Agent ID**: frontend-opus  
**Branch**: frontend-opus  
**Owned Paths**:

- `/frontend/**/*`
- UI/UX documentation in `/docs/ui/`
- Static assets and images

**Forbidden Paths**:

- `/backend/**/*` (owned by backend-opus)
- `/tests/**/*` (owned by test-opus)
- Server configuration files

## External Contracts

### Component Interface

All components must follow these patterns:

```typescript
// Props Interface
interface ComponentProps {
  data: DataType;
  onAction: (event: ActionEvent) => void;
  className?: string;
  testId?: string; // Required for test agent
}

// State Management
interface AppState {
  user: UserState;
  ui: UIState;
  data: DataState;
  error: ErrorState | null;
}
```

### API Integration

```typescript
// API Client Configuration
{
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:3001',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  }
}
```

### Design System

- Use consistent spacing: 4px base unit
- Color palette defined in `/frontend/src/styles/theme`
- Responsive breakpoints: 640px, 768px, 1024px, 1280px
- Accessibility: WCAG 2.1 AA compliance

## Definition of Done

✅ **All component tests pass** (`npm test`)  
✅ **E2E tests pass** (if implemented)  
✅ **No TypeScript errors** (`npm run typecheck`)  
✅ **No linting errors** (`npm run lint`)  
✅ **Responsive design verified** (mobile, tablet, desktop)  
✅ **Accessibility audit passes** (aXe or similar)  
✅ **Loading states implemented**  
✅ **Error states handled gracefully**  
✅ **Form validation working**  
✅ **CI pipeline green**

## Interface with Siblings

### Backend Dependencies

Wait for backend to provide:

1. API endpoint documentation
2. Authentication flow details
3. WebSocket events (if applicable)
4. File upload endpoints

### Test Agent Requirements

Provide for test agent:

1. Component `testId` attributes
2. Page object selectors
3. User flow documentation
4. Performance metrics

## Git Commit Format

All commits must follow this format:

```
[frontend-opus] <type>: <description>

<optional body>

<optional footer>
```

Types:

- `feat`: New feature/component
- `fix`: Bug fix
- `style`: UI/CSS changes
- `refactor`: Code restructuring
- `test`: Adding tests
- `docs`: Documentation updates
- `perf`: Performance improvements
- `a11y`: Accessibility improvements

Examples:

```
[frontend-opus] feat: create user profile component
[frontend-opus] fix: resolve navigation menu z-index issue
[frontend-opus] a11y: add ARIA labels to form inputs
```

## Additional Guidelines

1. **Component Architecture**:
   - Use functional components with hooks
   - Keep components small and focused
   - Extract reusable logic into custom hooks
   - Use composition over inheritance

2. **State Management**:
   - Local state for component-specific data
   - Global state for app-wide data
   - Avoid prop drilling beyond 2 levels
   - Use context sparingly

3. **Performance**:
   - Lazy load routes and heavy components
   - Optimize images (WebP, proper sizing)
   - Minimize bundle size
   - Use React.memo for expensive renders

4. **Styling**:
   - CSS modules or styled-components
   - Mobile-first approach
   - Use CSS variables for theming
   - Avoid inline styles

5. **User Experience**:
   - Show loading indicators
   - Provide feedback for actions
   - Handle offline scenarios
   - Implement proper error boundaries

6. **Testing Priority**:
   - User interactions
   - Form submissions
   - Navigation flows
   - Error scenarios
   - Accessibility features
