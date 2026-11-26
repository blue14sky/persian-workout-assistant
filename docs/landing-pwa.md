# Landing page / PWA

The home route (`/`) renders the Persian RTL mobile-first Fito landing page. It is explicitly an **early product concept**; the workout data-entry features shown in the illustrative phone mockup are not implemented.

## Routes
- `/`: public landing page
- `/join/`: POST-only early-access signup (Django CSRF protected)
- `/health/`: health endpoint; returns `{"status":"ok"}`
- `/manifest.webmanifest`: PWA manifest
- `/sw.js`: service worker

## UI and asset delivery
Django templates: `landing/templates/landing/index.html`. CSS, JS, and SVG icons: `landing/static/landing/`. WhiteNoise serves collected static assets without a second frontend container; the Dockerfile runs `collectstatic`.

App is reachable only through Docker's external `public_proxy` network (`workout-fito:8000`). There is no host port mapping. Nginx lives in `amdkna/nginx-edge-noyan`.

## Lead capture
The `EarlyAccessSignup` model stores a normalized, unique email and signup timestamp in PostgreSQL. The form requires consent, uses CSRF protection, validates email and includes a honeypot field. No bulk-email system, unsubscribe endpoint, or dashboard is implemented yet. Do not send marketing emails without adding a removal mechanism and appropriate email workflow. Avoid sharing users' addresses in logs.

## Verification
```bash
docker compose exec -T web python manage.py check
docker compose exec -T web python manage.py test landing
docker compose exec -T web python manage.py showmigrations landing
docker exec edge_nginx wget -S -O- --header='Host: workout.webigram.ir' http://workout-fito:8000/
curl -I -H 'Host: workout.webigram.ir' http://127.0.0.1/
curl -i -H 'Host: workout.webigram.ir' http://127.0.0.1/manifest.webmanifest
```

## PWA prerequisite
Browsers require HTTPS (or localhost) to register service workers and offer installation. The current `workout.webigram.ir` Nginx config is **HTTP-only**. Landing functionality works on HTTP, but PWA installation and offline behavior will require a valid TLS certificate and HTTPS vhost before public release. SVG icons are included; PNG icons may improve platform compatibility later.
