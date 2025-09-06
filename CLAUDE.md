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

### Database Migrations (sql-migrate)
```bash
# Navigate to migrations directory
cd services/api/infrastructure/migrations

# Create new migration file
sql-migrate new {migration_name}  # Example: sql-migrate new auth

# Apply migrations
sql-migrate up -env=development

# Rollback migrations
sql-migrate down -env=development

# Check migration status
sql-migrate status -env=development
```

**Important Rules**:
1. Always use `sql-migrate new` command to create migration files. Do not create migration SQL files manually.

2. **Database-specific considerations**:
   - Check docker-compose.yml or docker/ directory to determine which database is being used
   - **MySQL**: 
     - `updated_at` columns automatically update with `ON UPDATE CURRENT_TIMESTAMP` clause
     - No trigger needed for updated_at columns
     - UUID generation: Use `DEFAULT (UUID())`
   - **PostgreSQL**: 
     - Requires triggers for automatic updated_at column updates
     - UUID generation: Use `DEFAULT gen_random_uuid()`
     - Use `-- +migrate StatementBegin` and `-- +migrate StatementEnd` for triggers/functions

3. For PostgreSQL triggers and functions, use the following format:
```sql
-- +migrate StatementBegin
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';
-- +migrate StatementEnd

-- +migrate StatementBegin
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
-- +migrate StatementEnd
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

## Sub-Agent Task Assignment Guidelines

### Overview
This project utilizes specialized sub-agents located in `.claude/agents/` to handle specific technical domains. Each agent has expertise in their area and should be assigned tasks based on the criteria below.

### Agent Responsibilities and Selection Criteria

#### **backend-developer**
- **Assign when**: Python dependency issues, API endpoint errors, backend code implementation, database connection problems, unit test creation, SQLAlchemy model changes
- **Example tasks**: Fixing missing Python packages, implementing FastAPI routes, resolving database driver issues, writing pytest tests, optimizing query performance  
- **Decision point**: If the error is in Python code, involves FastAPI/SQLAlchemy, requires pip package management, or needs backend testing
- **Key expertise**: Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic, pytest, database migrations

#### **infrastructure-engineer**
- **Assign when**: Docker configuration issues, Cloud Run deployment, Terraform changes, GCP resource provisioning, CI/CD pipeline problems, Secret Manager configuration
- **Example tasks**: Docker compose configuration, Cloud Build setup, Terraform module creation, load balancer configuration, service account permissions
- **Decision point**: If the error involves containers, cloud infrastructure, deployment pipelines, or requires GCP resource management
- **Key expertise**: Docker, Terraform, GCP (Cloud Run, Cloud Build), GitHub Actions, container orchestration

#### **system-designer**
- **Assign when**: Need detailed design before implementation, complex feature breakdown, API contract design, acceptance criteria definition, system flow documentation
- **Example tasks**: Creating component specifications, defining test scenarios, designing data flow diagrams, breaking down user stories
- **Decision point**: If the task needs architectural planning, detailed specifications, or design documentation before implementation
- **Key expertise**: System architecture, UML diagrams, API design, test planning, acceptance criteria

#### **tech-architect**
- **Assign when**: Technology stack decisions, system-wide architecture changes, coding standards definition, integration strategy, performance optimization architecture
- **Example tasks**: Framework selection, microservice boundaries, establishing coding conventions, security architecture, scalability planning
- **Decision point**: If the decision affects multiple services, requires architectural patterns, or establishes project-wide standards
- **Key expertise**: Distributed systems, security patterns, performance optimization, technology evaluation

#### **quality-reviewer**
- **Assign when**: Code review needed, implementation verification, standards compliance check, security vulnerability assessment, performance review
- **Example tasks**: Reviewing PRs, checking code quality metrics, verifying test coverage, identifying security issues, ensuring documentation completeness
- **Decision point**: After implementation is complete and needs quality assessment or when establishing quality gates
- **Key expertise**: Code review best practices, security analysis, performance profiling, testing strategies

#### **product-manager**
- **Assign when**: Feature prioritization, user story creation, requirement clarification, stakeholder communication planning, roadmap definition
- **Example tasks**: Writing user stories, defining acceptance criteria from business perspective, prioritizing backlog, creating feature specifications
- **Decision point**: When business requirements need translation to technical specifications or priority decisions are needed
- **Key expertise**: Agile methodologies, user story mapping, requirement analysis, stakeholder management

#### **drawio-spec-converter**
- **Assign when**: Need to convert visual diagrams to technical specifications, architecture diagram interpretation, flow chart to code translation
- **Example tasks**: Converting draw.io diagrams to API specifications, translating flow charts to implementation plans, generating documentation from diagrams
- **Decision point**: When visual specifications need to be converted to actionable technical tasks
- **Key expertise**: Draw.io, diagram interpretation, specification generation, visual-to-code translation

### Task Assignment Best Practices

1. **Multiple Agent Collaboration**: Complex tasks may require multiple agents working in sequence
   - Example: system-designer → backend-developer → quality-reviewer

2. **Context Preservation**: When switching between agents, provide clear context including:
   - Previous agent's findings/implementation
   - Remaining tasks
   - Known constraints or issues

3. **Specialization Over Generalization**: Prefer specialist agents for their domain rather than having one agent handle everything

4. **Review Cycle**: For critical implementations, always include quality-reviewer as the final step

### Recent Task Assignment Examples
- **Database Driver Error (MySQLdb missing)**: Assigned to backend-developer
  - Reason: Python package dependency issue requiring pip install and requirements.txt update
- **Cloud Run Deployment Failure**: Assigned to infrastructure-engineer  
  - Reason: Container configuration and GCP service setup required
- **API Contract Design**: Assigned to system-designer → backend-developer
  - Reason: Needed specification first, then implementation

## Knowledge Management System

### Overview
各サブエージェントは専門領域のナレッジを `.claude/knowledge/` ディレクトリに蓄積し、過去の実装経験を活用して開発効率と品質を向上させます。

### Knowledge Base Structure

#### Directory Organization
```
.claude/
├── agents/           # Agent definition files
└── knowledge/        # Accumulated knowledge base
    ├── backend-developer-knowledge.md
    ├── infrastructure-engineer-knowledge.md
    ├── system-designer-knowledge.md
    ├── tech-architect-knowledge.md
    ├── quality-reviewer-knowledge.md
    ├── product-manager-knowledge.md
    └── drawio-spec-converter-knowledge.md
```

#### Knowledge Base Content Categories

- **backend-developer-knowledge.md**:
  - Python/FastAPI patterns, common errors and solutions
  - Database optimization techniques
  - Testing strategies and fixtures
  - Performance tuning discoveries

- **infrastructure-engineer-knowledge.md**:
  - Docker optimization techniques
  - Terraform module patterns
  - GCP service configurations
  - CI/CD pipeline optimizations

- **system-designer-knowledge.md**:
  - Design patterns used in the project
  - Component interaction diagrams
  - API design decisions and rationale
  - Test scenario templates

- **tech-architect-knowledge.md**:
  - Technology selection criteria and decisions
  - Architecture patterns and anti-patterns observed
  - Integration strategies that worked/failed
  - Performance benchmarks and limits

- **quality-reviewer-knowledge.md**:
  - Common code review findings
  - Security vulnerability patterns
  - Performance bottlenecks identified
  - Quality metrics and thresholds

- **product-manager-knowledge.md**:
  - User feedback patterns
  - Feature prioritization frameworks
  - Requirement clarification templates
  - Stakeholder communication strategies

### Knowledge Recording Rules

1. **Timing**: Record knowledge immediately after task completion while context is fresh

2. **Structure**: Each entry must include:
   ```markdown
   ## [Date] - [Task/Issue Title]
   
   ### Context
   Brief description of the situation
   
   ### Problem
   Specific issue encountered
   
   ### Root Cause
   Why the problem occurred
   
   ### Solution
   How it was resolved (include code/commands)
   
   ### Prevention
   How to avoid this in the future
   
   ### Related Knowledge
   Links to other relevant knowledge entries
   ```

3. **Code Examples**: Always include actual code snippets, not pseudocode

4. **Versioning**: Note relevant versions (Python, Node.js, GCP services) when applicable

5. **Cross-references**: Link related entries across different agent knowledge bases

### Knowledge Usage Protocol

1. **Pre-task Review**:
   - Agents must check their knowledge base before starting tasks
   - Search for similar problems and apply proven solutions

2. **Knowledge Application**:
   - Adapt previous solutions to current context
   - Validate that conditions match before applying stored solutions

3. **Continuous Update**:
   - Update existing entries if better solutions are found
   - Mark deprecated solutions clearly

4. **Knowledge Sharing**:
   - Reference other agents' knowledge when relevant
   - Create cross-agent knowledge links for complex solutions

### Knowledge Quality Standards

- **Accuracy**: Verify solutions work before documenting
- **Completeness**: Include all necessary context for reproduction
- **Clarity**: Write for future readers who may lack current context
- **Relevance**: Focus on reusable patterns, not one-off fixes
- **Maintenance**: Review and update quarterly or when major changes occur