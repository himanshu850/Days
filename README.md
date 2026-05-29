# Days Counter — Fly Deployment

This repository runs a small HTTP server that displays the number of days since a reference date.

Quick start

1. Update `fly.toml` and set `app = "your-fly-app-name"`.
2. Add a repository secret named `FLY_API_TOKEN` with a Fly personal access token.
3. Push to the `main` (or `master`) branch — GitHub Actions will build and deploy automatically.

Files added by the deploy automation:

- `Dockerfile` — containerizes the app using Python 3.11.
- `fly.toml` — Fly config template, update the `app` value.
- `.github/workflows/fly-deploy.yml` — CI/CD pipeline that deploys on push.
- `requirements.txt` — add Python dependencies if needed.

Notes

- The app listens on port `5000` internally; Fly routes HTTP to port `80` and to the internal port defined in `fly.toml`.
- Ensure `FLY_API_TOKEN` is set in your GitHub repo secrets. You can create the token at https://fly.io/dashboard/personal_access_tokens
