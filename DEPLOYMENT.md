# Fito deployment

The application is a Django/Gunicorn service with PostgreSQL, managed by Docker Compose.

## First deployment

GitHub Actions deploys on pushes to `main`, using the self-hosted runner labelled `wbg-test`.

The runner user must:
- Be able to write to `/opt/apps/azin-workout`.
- Be allowed to run Docker commands (normally by having Docker group access).
- Have Docker Engine with the Docker Compose v2 plugin installed.
- Have `openssl` installed for the first deployment.

The workflow creates `.env` on the first deployment and preserves it on later deployments. It does not run destructive cleanup commands.

After the first deployment, edit `/opt/apps/azin-workout/.env` and set:
- `DJANGO_ALLOWED_HOSTS`: your actual domain name(s), comma-separated, without the scheme.
- `CSRF_TRUSTED_ORIGINS`: your HTTPS origin(s), including the scheme, e.g. `https://fit.example.com`.

Then restart:

```bash
cd /opt/apps/azin-workout
docker compose up -d
```

## Existing Nginx

Nginx remains responsible for ports 80 and 443. In the relevant HTTPS virtual host, proxy requests to localhost port 8000:

```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Keep your existing TLS certificate and HTTP-to-HTTPS redirect configuration. Validate and reload Nginx after editing its site configuration.

## Test

- Home: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/health/`

The home endpoint returns JSON: `{"message":"Hello, world!","app":"Fito"}`.
