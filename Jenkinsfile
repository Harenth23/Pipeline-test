peline {
    agent any

    environment {
        VENV = '.venv'
        MONGO_CONTAINER = 'mongo-test'
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

        stage('Setup MongoDB') {
            steps {
                sh '''
                    docker run -d \
                      --name $MONGO_CONTAINER \
                      -p $MONGO_PORT:27017 \
                      -e MONGO_INITDB_DATABASE=todo_db \
                      mongo:6

                    echo "Waiting for MongoDB to be ready..."
                    for i in {1..10}; do
                        if docker exec $MONGO_CONTAINER mongo --eval "db.stats()" >/dev/null 2>&1; then
                            echo "MongoDB is up!"
                            break
                        fi
                        sleep 3
                    done
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt -r requirements-dev.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    flake8 app/
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    export PYTHONPATH=$PWD
                    pytest
                '''
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

                    echo "Waiting for FastAPI to be ready..."
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
