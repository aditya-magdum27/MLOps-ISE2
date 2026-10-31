# LAB-ISE2: CI/CD Pipeline and Monitoring Tools (Documentation Notes)

Use this to fill in the lab template (LAB-ISE2-CICD pipeline and Monitoring Tools). Add your own screenshots at each "Verify" step.

## 1. Problem statement

Build an Iris species classification web application (Flask + scikit-learn) and automate its test, build and deployment using a CI/CD pipeline (GitHub Actions + Jenkins + Docker), with runtime monitoring through Prometheus and Grafana.

## 2. Tools and versions

| Tool | Purpose |
|------|---------|
| Python 3.11 + Flask | Web application and ML model serving |
| scikit-learn | RandomForest model |
| Git and GitHub | Version control and remote repository |
| GitHub Actions | CI on every push |
| Jenkins | CI/CD pipeline automation |
| Docker / Docker Compose | Containerisation and multi-service deployment |
| Prometheus | Metrics collection |
| Grafana | Metrics dashboards |

## 3. Installation and verification

**Python / Flask**
```bash
python --version
pip install -r requirements.txt
python train_model.py
python app.py
```
Verify: open http://localhost:5000, submit values, see a predicted species. (Screenshot)

**Git / GitHub**
```bash
git --version
git init
git remote add origin https://github.com/aditya-magdum27/MLOps-ISE2.git
git add .
git commit -m "Add MLOps ISE-2 project"
git push -u origin main
```
Verify: files visible on GitHub. (Screenshot)

**Docker**
```bash
docker --version
docker build -t iris-mlops-app .
docker run -p 5000:5000 iris-mlops-app
```
Verify: app reachable at http://localhost:5000. (Screenshot of `docker ps`)

**Jenkins**
```bash
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins jenkins/jenkins:lts
```
(You can also install Jenkins directly on your machine.)
- Open http://localhost:8080 and unlock with `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword`.
- Install suggested plugins, then add the Git, Pipeline and Docker Pipeline plugins.
- Make sure Python 3, pip, venv, Docker CLI and curl are available on the Jenkins agent.
- New Item, Pipeline, "Pipeline script from SCM", Git, repo URL, branch `main`, script path `Jenkinsfile`.
- Build Now. Verify: all stages are green in Stage View. (Screenshot)

**Prometheus and Grafana**
```bash
docker compose up -d --build
```
- Prometheus: http://localhost:9090, Status, Targets, `iris-flask-app` should be UP. (Screenshot)
- Sample queries: `app_requests_total`, `rate(app_requests_total[1m])`, `app_predictions_total`.
- Grafana: http://localhost:3000 (admin/admin), Add data source, Prometheus, URL `http://prometheus:9090`, then create a dashboard with the queries above. (Screenshot)

## 4. CI/CD pipeline explanation

| Stage | What it does |
|-------|--------------|
| Checkout | Pulls the latest code from GitHub |
| Install Dependencies | Creates a venv and installs requirements |
| Train Model | Runs `train_model.py` |
| Run Tests | Runs pytest (health, predict, error handling, metrics) |
| Build Docker Image | Builds a tagged image |
| Smoke Test Container | Runs the container and calls `/health` |
| Deploy with Monitoring | `docker compose up -d` starts app, Prometheus and Grafana |

## 5. Monitoring metrics

- `app_requests_total{method,endpoint,status}`: request count
- `app_request_latency_seconds`: latency histogram
- `app_predictions_total{species}`: predictions per class

## 6. Conclusion

The project demonstrates an end-to-end MLOps workflow: code to GitHub, automated testing and Docker build through GitHub Actions and Jenkins, containerised deployment, and real-time monitoring with Prometheus and Grafana.
