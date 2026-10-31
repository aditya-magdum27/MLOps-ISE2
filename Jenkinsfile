pipeline {
    agent any

    environment {
        IMAGE_NAME = 'iris-mlops-app'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                    . venv/bin/activate
                    python train_model.py
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Smoke Test Container') {
            steps {
                sh '''
                    docker rm -f iris-smoke || true
                    docker run -d --name iris-smoke -p 5001:5000 ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 8
                    curl -f http://localhost:5001/health
                '''
            }
            post {
                always {
                    sh 'docker rm -f iris-smoke || true'
                }
            }
        }

        stage('Deploy with Monitoring') {
            steps {
                sh '''
                    docker compose up -d --build
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded: app on :5000, Prometheus on :9090, Grafana on :3000'
        }
        failure {
            echo 'Pipeline failed. Check the stage logs above.'
        }
    }
}
