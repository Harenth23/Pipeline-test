pipeline {
    agent any

    environment {
        VENV = '.venv'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Harenth23/Pipeline-test.git'

            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                pip install -r requirements.txt -r requirements-dev.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                . .venv/bin/activate
                flake8 app/
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                . .venv/bin/activate
                pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fastapi-todo-app .'
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
    }
}
