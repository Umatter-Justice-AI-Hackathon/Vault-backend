# Frontend Integration Guide

## Quick Start

**Backend API Base URL:**
- Development: `http://localhost:8000`
- Production: `https://your-app.onrender.com`

**API Documentation:**
- Swagger UI: `{BASE_URL}/api/v1/docs`
- ReDoc: `{BASE_URL}/api/v1/redoc`

## Authentication

### OAuth Flow

We support Google, GitHub, and Microsoft OAuth2.

**1. Initiate OAuth (Frontend)**
```typescript
// Redirect user to OAuth provider
window.location.href = `${API_BASE_URL}/api/v1/auth/{provider}/login`;
// where provider is: google, github, or microsoft
```

**2. Callback Handling (Backend → Frontend)**
```typescript
// Backend redirects to: {FRONTEND_URL}/auth/callback?token={jwt_token}
// Frontend should extract token from URL and store it
const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');
localStorage.setItem('authToken', token);
```

**3. Using the Token**
```typescript
// Include in all API requests
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

## API Endpoints

### Health Check
```
GET /health
Response: { status: "healthy", services: {...} }
```

### Authentication

#### Start OAuth Flow
```
GET /api/v1/auth/{provider}/login
Providers: google | github | microsoft
Redirects to OAuth provider
```

#### Get Current User
```
GET /api/v1/auth/me
Headers: Authorization: Bearer {token}
Response: {
  id: number,
  email: string,
  full_name: string,
  provider: string,
  created_at: string,
  last_login: string
}
```

#### Logout
```
POST /api/v1/auth/logout
Headers: Authorization: Bearer {token}
Response: { message: "Logged out successfully" }
```

### Chat Sessions

#### Start New Session
```
POST /api/v1/sessions
Headers: Authorization: Bearer {token}
Response: {
  id: number,
  user_id: number,
  started_at: string,
  wellbeing_score: null
}
```

#### Get User's Sessions
```
GET /api/v1/sessions
Headers: Authorization: Bearer {token}
Query Params:
  - limit: number (default: 20)
  - offset: number (default: 0)
Response: {
  sessions: [{
    id: number,
    started_at: string,
    ended_at: string | null,
    wellbeing_score: number | null,
    session_summary: string | null
  }],
  total: number
}
```

#### Get Session Details
```
GET /api/v1/sessions/{session_id}
Headers: Authorization: Bearer {token}
Response: {
  id: number,
  started_at: string,
  ended_at: string | null,
  wellbeing_score: number | null,
  session_summary: string | null,
  action_plan: string | null,
  messages: [{
    id: number,
    role: "user" | "assistant" | "system",
    content: string,
    timestamp: string
  }]
}
```

#### End Session
```
POST /api/v1/sessions/{session_id}/end
Headers: Authorization: Bearer {token}
Response: {
  id: number,
  ended_at: string,
  wellbeing_score: number,
  session_summary: string
}
```

### Chat Messages

#### Send Message
```
POST /api/v1/chat
Headers: Authorization: Bearer {token}
Body: {
  message: string,           // User's message (1-10000 chars)
  session_id?: number        // Optional: use existing session
}
Response: {
  session_id: number,
  message: string,           // AI response
  wellbeing_score: number | null,
  requires_intervention: boolean,
  intervention_type: "breathing" | "grounding" | null
}
```

**Note:** If `requires_intervention` is true, the frontend should display a breathing exercise or grounding technique UI.

### Analytics

#### Get Wellbeing Trend
```
GET /api/v1/analytics/trend
Headers: Authorization: Bearer {token}
Query Params:
  - days: number (default: 30)
Response: {
  data_points: [{
    date: string,
    average_wellbeing_score: number | null,
    session_count: number,
    total_messages: number
  }],
  trend: "improving" | "declining" | "stable",
  recommendation: string | null
}
```

#### Get Session Score History
```
GET /api/v1/analytics/scores
Headers: Authorization: Bearer {token}
Query Params:
  - limit: number (default: 30)
Response: [{
  date: string,
  score: number
}]
```

### Action Plans

#### Generate Action Plan
```
POST /api/v1/sessions/{session_id}/action-plan
Headers: Authorization: Bearer {token}
Response: {
  session_id: number,
  generated_at: string,
  actions: [{
    title: string,
    description: string,
    priority: "high" | "medium" | "low",
    category: "workplace" | "personal" | "professional_help"
  }],
  summary: string
}
```

#### Get User's Action Plans
```
GET /api/v1/action-plans
Headers: Authorization: Bearer {token}
Response: [{
  session_id: number,
  generated_at: string,
  actions: [...],
  summary: string
}]
```

## Data Models

### User
```typescript
interface User {
  id: number;
  email: string;
  full_name: string | null;
  provider: "google" | "github" | "microsoft";
  created_at: string; // ISO 8601
  last_login: string;  // ISO 8601
  is_active: boolean;
}
```

### Session
```typescript
interface Session {
  id: number;
  user_id: number;
  started_at: string;
  ended_at: string | null;
  wellbeing_score: number | null;  // 0-10 scale
  session_summary: string | null;
  action_plan: string | null;
}
```

### Message
```typescript
interface Message {
  id: number;
  session_id: number;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: string;
}
```

### ChatResponse
```typescript
interface ChatResponse {
  session_id: number;
  message: string;
  wellbeing_score: number | null;
  requires_intervention: boolean;
  intervention_type: "breathing" | "grounding" | null;
}
```

### ActionPlan
```typescript
interface ActionItem {
  title: string;
  description: string;
  priority: "high" | "medium" | "low";
  category: "workplace" | "personal" | "professional_help";
}

interface ActionPlan {
  session_id: number;
  generated_at: string;
  actions: ActionItem[];
  summary: string;
}
```

### Analytics
```typescript
interface DataPoint {
  date: string;
  average_wellbeing_score: number | null;
  session_count: number;
  total_messages: number;
}

interface WellbeingTrend {
  data_points: DataPoint[];
  trend: "improving" | "declining" | "stable";
  recommendation: string | null;
}
```

## Error Handling

All errors follow this format:

```typescript
interface APIError {
  detail: string | {
    msg: string;
    type: string;
    loc?: string[];
  }[];
}
```

**HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `422` - Validation Error (Pydantic validation)
- `500` - Internal Server Error

**Example Error Response:**
```json
{
  "detail": "Invalid authentication credentials"
}
```

**Validation Error Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Frontend Implementation Checklist

### Authentication
- [ ] Implement OAuth redirect flow
- [ ] Store JWT token securely (localStorage or httpOnly cookie)
- [ ] Refresh token on expiry (implement token refresh endpoint)
- [ ] Handle logout (clear token, redirect to login)
- [ ] Protect routes (redirect to login if not authenticated)

### Chat Interface
- [ ] Display chat messages (user vs assistant styling)
- [ ] Send user messages
- [ ] Handle streaming responses (if implemented)
- [ ] Show typing indicator while waiting for response
- [ ] Display wellbeing score indicator
- [ ] Show intervention UI when `requires_intervention` is true

### Session Management
- [ ] Create new session on first message
- [ ] List previous sessions (with dates and scores)
- [ ] Resume existing session
- [ ] End session with summary

### Wellbeing Tracking
- [ ] Display current session score
- [ ] Show score trend chart (last 30 days)
- [ ] Show session history with emoji representation
- [ ] Color-code UI based on mood/score

### Action Plans
- [ ] Generate action plan button
- [ ] Display action items categorized by priority
- [ ] Mark actions as complete (future feature)
- [ ] View all action plans

### Interventions
- [ ] Breathing exercise component (animated)
- [ ] Grounding technique component (5-4-3-2-1 method)
- [ ] Trigger interventions when backend recommends

### UI/UX Requirements
- [ ] Responsive design (mobile-first)
- [ ] Accessible (ARIA labels, keyboard navigation)
- [ ] Loading states
- [ ] Error states with user-friendly messages
- [ ] Empty states (no sessions, no action plans)
- [ ] Smooth transitions and animations

## Best Practices

### Security
1. **Never** store sensitive data in localStorage unencrypted
2. Always use HTTPS in production
3. Validate all user inputs on frontend AND backend
4. Implement CSRF protection if using cookies
5. Set appropriate CORS headers

### Performance
1. Implement pagination for lists (sessions, messages)
2. Cache user data after login
3. Debounce chat input to prevent spam
4. Lazy load chat history
5. Optimize images and assets

### User Experience
1. Show real-time feedback (typing indicators, loading states)
2. Handle errors gracefully with helpful messages
3. Implement offline mode with queued messages (future feature)
4. Auto-save draft messages
5. Provide clear navigation and breadcrumbs

### Accessibility
1. Use semantic HTML
2. Provide alt text for all images
3. Ensure keyboard navigation works
4. Use ARIA labels for dynamic content
5. Maintain color contrast ratios (WCAG AA)

## Example Frontend Code

### Authentication Hook (React)
```typescript
// hooks/useAuth.ts
import { useState, useEffect } from 'react';

interface User {
  id: number;
  email: string;
  full_name: string;
}

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      fetch('http://localhost:8000/api/v1/auth/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(data => setUser(data))
        .catch(() => localStorage.removeItem('authToken'))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = (provider: 'google' | 'github' | 'microsoft') => {
    window.location.href = `http://localhost:8000/api/v1/auth/${provider}/login`;
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setUser(null);
  };

  return { user, loading, login, logout };
};
```

### Chat API Client (React)
```typescript
// api/chat.ts
const API_BASE = 'http://localhost:8000/api/v1';

export const sendMessage = async (message: string, sessionId?: number) => {
  const token = localStorage.getItem('authToken');
  
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message, session_id: sessionId })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return response.json();
};
```

## Environment Variables

Frontend should have:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_VERSION=v1

# OAuth Redirect (must match backend configuration)
VITE_AUTH_CALLBACK_URL=http://localhost:3000/auth/callback
```

## CORS Configuration

The backend is configured to allow requests from:
- `http://localhost:3000` (development)
- Your production frontend URL (set via `FRONTEND_URL` env var)

All standard headers and methods are allowed.

## WebSocket Support (Future)

Currently not implemented. For real-time features, we'll add:
```
WS /api/v1/chat/stream
```

## Questions or Issues?

- Check API docs at `/api/v1/docs`
- Review this document
- Ask in team Slack/Discord
- Open an issue on GitHub

## Testing

Backend provides test data endpoints (development only):
```
POST /api/v1/dev/seed-data  # Create test user and sessions
DELETE /api/v1/dev/clear-data  # Clear all test data
```

Use these for frontend development and testing.
