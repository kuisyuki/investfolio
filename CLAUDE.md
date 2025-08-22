# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

InvestFolio is a portfolio management system learning project built with Clean Architecture principles. It consists of a FastAPI backend and a Next.js frontend, designed as an educational platform for implementing financial portfolio management features.

## Development Commands

### Frontend (Next.js)
```bash
cd services/web
npm run dev          # Start development server on port 3000
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

### Backend (FastAPI)
```bash
cd services/api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000  # Start development server

# Code quality tools
black .              # Code formatting
isort .              # Import sorting
ruff .               # Linting
```

### Testing
```bash
# Backend tests (run from repository root)
pytest tests/services/api

# Test configuration is in services/api/pytest.ini
# Tests are located in tests/services/api/
```

## Architecture

### Backend (Clean Architecture)
- **Domain Layer**: Core business entities and rules
  - `domain/entities/`: Business entities (User, Portfolio, Stock, Transaction)
  - `domain/repositories/`: Repository interfaces
  - `domain/services/`: Domain services
- **Application Layer**: Use cases and application logic
  - `application/use_cases/`: Business use cases
  - `application/dto/`: Data transfer objects
- **Infrastructure Layer**: External concerns
  - `infrastructure/repositories/`: Repository implementations
  - `infrastructure/database/`: Database configuration
  - `infrastructure/external/`: External API integrations
- **Presentation Layer**: API interfaces
  - `presentation/routes/`: FastAPI route handlers
  - `presentation/schemas/`: Request/response schemas
  - `presentation/middlewares/`: HTTP middlewares

### Frontend (Next.js)
- App Router structure in `services/web/app/`
- Components in `app/components/`
- Context providers in `app/contexts/`
- Pages: login, register, portfolio, transactions, analysis

### Key Dependencies
- **Backend**: FastAPI, SQLAlchemy, Pydantic, pytest
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, React Query, Zustand

## Current Implementation Status

### Completed Features
- Health check API endpoint (`/health`)
- Mock stock price API (`/api/stocks/nintendo`)
- Basic Clean Architecture structure
- Frontend UI for login/register (non-functional)
- Homepage with feature overview

### Planned Features (Learning Objectives)
- User authentication (JWT)
- Portfolio management
- Transaction tracking
- Real-time stock data integration
- Performance analytics
- Data visualization

## Development Notes

- CORS is configured for development (allows all origins)
- Stock data currently uses mock repository returning fixed Nintendo price
- Database models exist but are not yet integrated
- Authentication system is structured but not implemented
- Tests are configured but minimal coverage currently

## API Documentation
FastAPI auto-generates documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc