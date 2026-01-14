# Todo App Frontend

Next.js 16+ frontend for Todo App with Better Auth.

## Architecture

- **Framework**: Next.js 16+ (App Router)
- **UI**: React 19 with TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT tokens
- **Node**: 20+

## Project Structure

```
frontend/
├── src/
│   ├── app/             # Next.js 16+ App Router pages
│   ├── components/      # Reusable React components
│   └── lib/             # Utilities, API clients, auth config
├── tests/               # Component and integration tests
├── package.json         # Node dependencies
├── .env.example         # Environment variable template
└── README.md            # This file
```

## Setup

1. Install dependencies:
```bash
npm install
```

2. Copy `.env.example` to `.env.local`:
```bash
cp .env.example .env.local
```

3. Configure environment variables in `.env.local`

4. Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

## Development

- Follow ESLint + Prettier rules
- Use TypeScript for type safety
- Use functional React components
- Separate presentation from business logic
- Run linter: `npm run lint`
- Type check: `npm run type-check`

## Constitution Compliance

This frontend follows the Todo App Constitution v2.0.0:
- ✅ Principle III: Next.js 16+ App Router, Tailwind CSS
- ✅ Principle IV: TypeScript, functional components, proper separation
- ✅ Principle VII: Better Auth JWT authentication
