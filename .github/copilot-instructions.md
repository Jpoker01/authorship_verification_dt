# GitHub Copilot Instructions

## Project Overview

This repository contains a diploma thesis project on **Authorship Verification using Artificial Intelligence Methods**. The project explores various AI techniques to verify authorship of texts and provides a web application for practical use.

## Repository Structure

The project is organized into two main components:

### 1. Experiments (`/experiments`)
Contains Jupyter notebooks with AI experiments for authorship verification:
- `/notebooks/dataset` - Dataset processing and exploration
- `/notebooks/graph` - Experiments with integrated syntactic graphs
- `/notebooks/llm` - Large Language Model experiments
- `/notebooks/traditional` - Traditional BOW/TF-IDF approaches
- `/notebooks/transformer` - Transformer-based model experiments
- `/results` - Experiment results and analysis
- Naming convention for notebooks: `YYYYMMDD_developerinitials - description`

### 2. Web Application (`/webapp`)

#### Backend (`/webapp/backend`)
- **Framework**: FastAPI (Python)
- **Structure**:
  - `/routers` - API route handlers
  - `/schemas` - Pydantic schemas for request/response validation
  - `/core` - Core functionality (ML models, configuration)
  - `/internal` - Internal utilities
  - `main.py` - FastAPI application entry point

#### Frontend (`/webapp/frontend`)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **Key Dependencies**:
  - Supabase client for backend integration
  - Framer Motion for animations
  - Lucide React for icons

## Technology Stack

### Backend
- Python with FastAPI
- Pydantic for data validation
- Machine learning models for authorship verification

### Frontend
- React 18.3+
- TypeScript 5.5+
- Vite 5.4+ (build tool)
- TailwindCSS 3.4+ (styling)
- ESLint for code quality

### Data Science
- Jupyter Notebooks
- Various ML/AI frameworks for experiments
- MLFlow for experiment tracking

## Development Guidelines

### Frontend Development

#### Running the Frontend
```bash
cd webapp/frontend
npm install
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run typecheck    # TypeScript type checking
```

#### Frontend Code Style
- Use TypeScript for all new code
- Follow React best practices and hooks
- Use functional components
- Maintain ESLint configuration
- Use TailwindCSS for styling

### Backend Development

#### Running the Backend
```bash
cd webapp/backend
# Install dependencies (requirements.txt should be in parent or specific location)
python main.py       # Or uvicorn main:app --reload
```

#### Backend Code Style
- Follow FastAPI best practices
- Use Pydantic models for request/response validation
- Organize routes in `/routers` directory
- Keep business logic in `/core` directory
- Use type hints for all Python code

### Experiments

#### Working with Notebooks
- Place notebooks in appropriate subdirectories based on approach
- Follow naming convention: `YYYYMMDD_developerinitials - description`
- Document experiments thoroughly
- Store results in `/results` directory

## Best Practices

1. **Code Organization**: Keep related code together, follow existing directory structure
2. **Type Safety**: Use TypeScript in frontend and type hints in Python backend
3. **API Design**: Follow RESTful principles in FastAPI routes
4. **Validation**: Use Pydantic schemas for all API request/response models
5. **Styling**: Use TailwindCSS utility classes, avoid custom CSS when possible
6. **Testing**: Write tests for critical functionality (refer to existing test patterns)
7. **Documentation**: Document complex algorithms and model implementations
8. **Dependencies**: Keep dependencies minimal and up-to-date

## Common Tasks

### Adding a New API Endpoint
1. Create or update route handler in `/webapp/backend/routers`
2. Define Pydantic schemas in `/webapp/backend/schemas`
3. Update `/webapp/backend/main.py` if new router needs to be included

### Adding a New Frontend Component
1. Create component in appropriate directory under `/webapp/frontend/src`
2. Use TypeScript and functional components
3. Style with TailwindCSS
4. Ensure accessibility and responsiveness

### Running a New Experiment
1. Create notebook in appropriate `/experiments/notebooks` subdirectory
2. Follow naming convention
3. Document methodology and results
4. Export results to `/experiments/results`

## Notes for AI Assistants

- This is a research project combining academic experiments with a practical web application
- The experiments are exploratory and may contain various approaches
- The web application is the production deployment of the chosen model
- Maintain consistency with existing code patterns
- Prioritize code clarity and documentation for academic context
