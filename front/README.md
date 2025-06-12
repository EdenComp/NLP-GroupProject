# GitHub Handshake - Frontend

A Vue 3 + TypeScript application that finds the shortest path between two GitHub users through their connections.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
Create a `.env` file in the root directory with:
```
VITE_API_URL=http://localhost:5000
```

3. Start development server:
```bash
npm run dev
```

## API Integration

The application calls the backend API endpoint `GET /path/:user1/:user2` to fetch the connection path between two users. The API URL is configurable via the `VITE_API_URL` environment variable.

## Build

```bash
npm run build
```
