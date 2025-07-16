pipeline {
    agent any

    environment {
        VENV = '.venv'
        MONGO_CONTAINER = 'jenkins-mongo'
        MONGO_PORT = '27017'
        MONGO_URI = 'mongodb://localhost:27017'
        FASTAPI_CONTAINER = 'fastapi-todo-container'
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
                export PYTHONPATH=$PWD
                pytest
                '''
            }
        }

        stage('Setup MongoDB') {
            steps {
                sh '''
                    docker run -d \
                      --name mongo-test \
                      -p 27017:27017 \
                      -e MONGO_INITDB_DATABASE=todo_db \
                      mongo:6
                '''
                // Wait a bit for MongoDB to initialize
                sleep 10
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fastapi-todo-app .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker rm -f $FASTAPI_CONTAINER || true
                docker run -d --name $FASTAPI_CONTAINER \
                    -e MONGO_URI=$MONGO_URI \
                    -p 8000:8000 fastapi-todo-app
                sleep 5
                '''
            }
        }

        stage('Test API Endpoint') {
            steps {
                sh '''
                curl --fail http://localhost:8000/todos/ || (echo "App is not responding" && exit 1)
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
            sh '''
            docker rm -f $MONGO_CONTAINER || true
            docker rm -f $FASTAPI_CONTAINER || true
            '''
        }
    }
}
