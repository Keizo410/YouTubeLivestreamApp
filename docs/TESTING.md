# Testing Strategy

## Testing Layers

- Unit Tests (e.g. functions, services)
- Integration Tests (Flask <-> Celery <-> DB)
- End-to-End (Cypress – future)

## Tools

- `pytest`
- `Jest`, `React Testing Library`
- GitHub Actions for CI

## Commands

```bash
#run in docker container
docker ps 
#get postgres container #id
docker exec -it {containerId} pytest
