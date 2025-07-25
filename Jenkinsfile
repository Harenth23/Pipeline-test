pipeline {
    agent any

    environment {
        VENV = '.venv'
        MONGO_CONTAINER = 'mongo-test'
        MONGO_PORT = '27017'
        MONGO_URI = 'mongodb://mongo-test:27017'
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
                docker rm -f mongo-test || true
                docker run -d \
                    --name mongo-test \
                    -p 27017:27017 \
                    -e MONGO_INITDB_DATABASE=todo_db \
                    mongo:6

                echo "Waiting for MongoDB to be ready on localhost:27017..."

                for i in {1..10}; do
                    if nc -z localhost 27017; then
                        echo "MongoDB is up!"
                        break
                    else
                        echo "Mongo not ready yet... retrying in 3s"
                        sleep 3
                    fi
                done

            '''
            }
        }


    stage('Debug Environment') {
        steps {
            sh '''
                echo "Python3 Path:"
                which python3 || true

                echo "Python3 Version:"
                python3 --version || true

                echo "Python3 Modules Directory:"
                python3 -m site || true

                echo "Checking ensurepip..."
                python3 -m ensurepip --version || echo "ensurepip missing"

                echo "PATH Environment:"
                echo $PATH

                echo "User:"
                whoami
            '''
            }
        }


        stage('Test Venv Creation') {
            steps {
                sh '''
                    echo "Creating venv and checking contents..."
                    python3 -m venv testenv
                    ls -l testenv/bin || echo "testenv/bin not found"
                    ls -l testenv/bin/pip || echo "Pip not found"
                    testenv/bin/python --version || echo "Python in venv not found"
                '''
            }
       }

        stage('Install Dependencies') {
            steps {
                sh '''
                    set -e
                    VENV=".venv"
                    python3 -m venv $VENV
                    ls -l $VENV/bin
                    $VENV/bin/python -m ensurepip --upgrade
                    $VENV/bin/pip install --upgrade pip --break-system-packages
                    $VENV/bin/pip install --break-system-packages -r requirements.txt -r requirements-dev.txt
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
                    docker run --rm --network container:$MONGO_CONTAINER \
                    -v $PWD:/app -w /app python:3.12-bookworm bash -c '
                        set -e && 
                        apt-get update &&
                        apt-get install -y gcc libffi-dev python3-venv curl &&
                        python3 -m venv .venv &&
                        . .venv/bin/activate &&
                        pip install --upgrade pip &&
                        pip install -r requirements.txt -r requirements-dev.txt &&
                        export PYTHONPATH=/app &&
                        pytest'
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

        stage('Show FastAPI Logs') {
            steps {
                sh '''
                    echo "====== FastAPI Uvicorn Logs ======"
                    docker logs $FASTAPI_CONTAINER || true
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
                echo "====== FastAPI Logs (Post Stage) ======"
                docker logs $FASTAPI_CONTAINER || true
                docker rm -f $MONGO_CONTAINER || true
                docker rm -f $FASTAPI_CONTAINER || true
            '''
        }
    }
}
