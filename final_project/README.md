# Django Dockerized Project

This project is a Dockerized Django application.

### Running the Project

1. **Build and start the Docker containers:**

   ```sh
   docker-compose up --build
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```
### Open your web browser and go to http://localhost:8000.

## Troubleshooting

If you encounter any issues, try checking the container logs:

```sh
docker-compose logs
```
