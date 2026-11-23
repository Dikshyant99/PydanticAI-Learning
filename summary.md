# Zonely – Day 1 Notes

## What is Zonely?
A golf platform where people can find coaches, venues and players, join golf games, buy memberships and shop.

## Tech stack
- Backend: Go
- Frontend: React
- Database: PostgreSQL
- Payments: Stripe
- Runs with: Docker

## Main Folders

zonelyProduction/
├── cmd/server/main.go  : starts the backend, lists all API routes
├── internal/handlers/  : code for each API
├── internal/middleware/: checks login and user roles
├── db/                 : database tables and SQL queries
├── frontend/src/pages/ : website screens
├── frontend/src/services/ : frontend calls to the backend
└── docker-compose.yml  : runs everything locally


## How It Works

User clicks something on the website (React)
        
Frontend sends a request to /api/v1/
        
Backend (Go) checks the login and handles the request
        
Reads/saves data in the database
        
Sends the result back to the website

## Types of APIs
- Public: anyone can use (view events, venues, coaches, register, login)
- Logged in: need a login token (profile, payments, uploads)
- Members only: need an active membership (create/join games)
- Admin only: manage users, venues, shop, events

## Main Workflows
1. **Sign up** : verify phone with an SMS code → verify email
2. **Login** : get a token (valid for 24 hours)
3. **Buy membership** : pay with Stripe → membership becomes active
4. **Join a game** : pay with Stripe or account credit → booking confirmed

