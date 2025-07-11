pipeline {
    agent any

    environment {
        VENV = '.venv'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://your-repo-url.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv $VENV
                source $VENV/bin/activate
                pip install -r requirements.txt -r requirements-dev.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                source $VENV/bin/activate
                flake8 app/
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                source $VENV/bin/activate
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
