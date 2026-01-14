# ADR-002: Authentication with Better Auth and JWT

**Status**: Accepted
**Date**: 2026-01-05
**Deciders**: Architecture Team, Security Review
**Feature**: 002-phase2-fullstack-todo

## Context

Phase 2 requires multi-user authentication to enable user-scoped task data. Key requirements:

1. **User Registration & Login** (FR-001, FR-005): Email/password authentication
2. **Session Management** (FR-006): 7-day session persistence with configurable expiration
3. **Security** (FR-004, FR-008): Secure password storage, protection against brute force
4. **Multi-User Isolation** (FR-021-FR-027): Strict user-scoped data access
5. **Stateless Backend**: Horizontal scaling without shared session state
6. **Constitution Compliance**: Principle VII mandates JWT tokens with Better Auth

**Constraints**:
- Backend (FastAPI) and Frontend (Next.js) must share authentication mechanism
- JWT tokens must be validated by backend for every API request
- No centralized auth service initially (keeps MVP simple)
- HTTPS required in production

## Decision

Implement **Better Auth + JWT token** authentication architecture with the following components:

### Authentication Flow

```
┌──────────┐                ┌──────────┐                 ┌──────────┐
│ Frontend │                │ Better   │                 │ Backend  │
│ (Next.js)│                │ Auth     │                 │ (FastAPI)│
└────┬─────┘                └────┬─────┘                 └────┬─────┘
     │                           │                            │
     │ 1. User submits           │                            │
     │    email/password          │                            │
     ├──────────────────────────>│                            │
     │                           │                            │
     │                           │ 2. Validate credentials    │
     │                           │    Hash password           │
     │                           ├───────────────────────────>│
     │                           │                            │
     │                           │ 3. User record             │
     │                           │<───────────────────────────┤
     │                           │                            │
     │                           │ 4. Generate JWT token      │
     │                           │    with BETTER_AUTH_SECRET │
     │                           │    Payload: {sub: user_id} │
     │                           │                            │
     │ 5. JWT token + user data  │                            │
     │    Store in HTTP-only     │                            │
     │    cookie                 │                            │
     │<──────────────────────────┤                            │
     │                           │                            │
     │ 6. API request with       │                            │
     │    Authorization: Bearer  │                            │
     │    <JWT>                  │                            │
     ├────────────────────────────────────────────────────────>│
     │                           │                            │
     │                           │                            │ 7. Validate JWT
     │                           │                            │    with BETTER_AUTH_SECRET
     │                           │                            │    Extract user_id from payload
     │                           │                            │    Check user_id in path matches token
     │                           │                            │
     │ 8. API response           │                            │
     │<────────────────────────────────────────────────────────┤
```

### Components

**1. Frontend (Better Auth)**:
- Handles user registration/login UI
- Generates JWT tokens using `BETTER_AUTH_SECRET`
- Stores JWT in **HTTP-only cookies** (prevents XSS attacks)
- Automatically attaches JWT to API requests via `Authorization: Bearer <token>` header
- Implements logout by clearing cookie

**2. Backend (FastAPI)**:
- Validates JWT tokens using shared `BETTER_AUTH_SECRET`
- Extracts `user_id` from verified token payload (`sub` claim)
- FastAPI dependency injection: `get_current_user()` middleware
- Authorization check: Verifies `user_id` in URL path matches authenticated user
- Returns **401 Unauthorized** for invalid/missing tokens
- Returns **403 Forbidden** for valid token but wrong user_id

**3. Shared Secret**:
- `BETTER_AUTH_SECRET` stored in environment variables (never committed)
- HS256 algorithm for JWT signing (symmetric key)
- Secret rotation strategy for production

**4. Token Configuration**:
- Expiration: 7 days (10080 minutes) - configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`
- Payload: `{"sub": user_id, "exp": expiration_timestamp}`
- Algorithm: HS256

### Security Measures

✅ **Password Hashing**: Bcrypt with salt (FR-004)
✅ **HTTP-Only Cookies**: Prevents JavaScript access to tokens (XSS mitigation)
✅ **HTTPS Only**: Required in production (prevents token interception)
✅ **Token Expiration**: 7-day limit reduces compromise window
✅ **User-Scoped Authorization**: Every endpoint verifies user_id matches token

## Consequences

### Positive

✅ **Stateless Authentication**: JWT enables horizontal scaling without shared session storage (Redis, database)

✅ **Simple Integration**: Shared secret approach requires minimal infrastructure (no public key management)

✅ **Constitution Compliance**: Satisfies Principle VII mandate for JWT + Better Auth

✅ **Modern DX**: Better Auth provides excellent developer experience with minimal configuration

✅ **Security**: HTTP-only cookies + HTTPS prevent common attack vectors (XSS, MITM)

✅ **Fast Validation**: JWT validation is CPU-bound (no database lookup), sub-millisecond latency

### Negative

⚠️ **Token Revocation**: Cannot invalidate tokens before expiration (logout is client-side only)
- **Mitigation**: Keep expiration short (7 days), implement token blacklist if needed in future

⚠️ **Secret Rotation Complexity**: Rotating `BETTER_AUTH_SECRET` invalidates all active tokens
- **Mitigation**: Document rotation procedure, notify users of re-auth requirement

⚠️ **Cookie Size**: JWT tokens increase cookie payload (typically 200-500 bytes)
- **Acceptable**: Well within 4KB cookie limit, no performance impact

⚠️ **Shared Secret Compromise**: If secret leaks, attacker can forge any token
- **Mitigation**: Store in secure secret management (AWS Secrets Manager, etc.), never commit to git, rotate regularly

### Risks

🔴 **Risk**: Shared secret leakage enables token forgery
- **Mitigation**: Environment variables only, secret manager in production, regular rotation, alerts on suspicious auth patterns

🟡 **Risk**: JWT payload tampering attempts
- **Mitigation**: Signature verification catches tampering, returns 401 immediately

🟢 **Risk**: Session fixation attacks
- **Mitigation**: New token generated on every login, old tokens not reused

## Alternatives Considered

### Alternative 1: Session-Based Authentication with Redis

**Pros**:
- Instant token revocation (delete session from Redis)
- Familiar pattern for many developers
- Can store additional session data beyond user_id

**Cons**:
- **Stateful**: Requires Redis or database for session storage
- **Scaling Complexity**: Shared Redis instance becomes single point of failure
- **Performance**: Every request requires database/Redis lookup (~1-5ms overhead)
- **Infrastructure Cost**: Additional service to maintain

**Why Rejected**: Stateless JWT better aligns with horizontal scaling goals. Token revocation edge case doesn't justify Redis infrastructure complexity for MVP.

### Alternative 2: OAuth2 with Separate Auth Service

**Pros**:
- Industry standard protocol (OAuth2)
- Centralized auth logic, reusable across projects
- Supports third-party logins (Google, GitHub, etc.)

**Cons**:
- **Over-Engineered for MVP**: Adds significant complexity
- **Additional Service**: Requires deploying and maintaining separate auth service
- **Network Latency**: Backend must call auth service for every request validation
- **Development Overhead**: More configuration, more failure points

**Why Rejected**: MVP doesn't require third-party logins. Shared secret JWT is 80% simpler with 95% of the functionality.

### Alternative 3: Magic Link / Passwordless Auth

**Pros**:
- Better UX (no passwords to remember)
- Eliminates password compromise risk
- Modern authentication pattern

**Cons**:
- **Email Service Required**: Phase 2 explicitly excludes email functionality (out of scope)
- **Delayed Auth**: Users must wait for email, slower than immediate login
- **Email Deliverability**: Spam folders cause friction

**Why Rejected**: Requires email service (out of scope for Phase 2 per spec). Password-based auth is simpler MVP path.

## Implementation Details

### Backend FastAPI Dependency

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)) -> User:
    """Extract and validate user from JWT token."""
    try:
        payload = jwt.decode(
            token.credentials,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Fetch user from database
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Frontend Better Auth Config

```typescript
// lib/auth/better-auth.ts
import { createAuth } from 'better-auth'

export const auth = createAuth({
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL,
  database: {
    // Configured to use FastAPI backend
    provider: 'custom',
    customFetch: async (url, options) => {
      return fetch(`${process.env.NEXT_PUBLIC_API_URL}${url}`, options)
    }
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    cookieSecure: process.env.NODE_ENV === 'production'
  }
})
```

## References

- [Constitution v2.0.0 Principle VII](../../.specify/memory/constitution.md#principle-vii-multi-user-authentication--authorization)
- [Research: Better Auth + FastAPI JWT Integration](../../specs/002-phase2-fullstack-todo/research.md#2-better-auth--fastapi-jwt-integration)
- [Implementation Plan: Authentication Flow](../../specs/002-phase2-fullstack-todo/plan.md#technical-approach)
- [API Contract: Auth Endpoints](../../specs/002-phase2-fullstack-todo/contracts/api-spec.yaml)
- [OWASP JWT Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)

## Notes

- **Reversibility**: Medium difficulty. Switching to session-based auth would require Redis infrastructure and endpoint changes
- **Future Enhancements**: Token refresh mechanism, token blacklist for revocation, multi-factor authentication
- **Security Audit**: Recommend third-party security review before production deployment
