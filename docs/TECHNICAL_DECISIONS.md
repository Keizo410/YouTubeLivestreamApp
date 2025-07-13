# Technical Decisions

## Backend Stack

- **Flask** over FastAPI for flexibility
- **Celery + RabbitMQ** for async task handling
- **PostgreSQL** with normalized schema

## Infra & Tooling

- Dockerized for portability
- GitHub Actions for CI/CD
- Nginx + HTTPS (in production)

## Security (future feature)

- Rate limiting
- Input validation
- Webhook verification

## Performance (future feature)

- Indexing strategy in PostgreSQL
- Connection pooling
- Caching (future: Redis)