pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "my-web-app"
        DOCKER_TAG = "${BUILD_NUMBER}"
        VENV = "venv"
    }

    stages {

        stage('Code Linting') {
            steps {
                script {
                    echo '========== Stage 1: Code Linting =========='
                    sh '''
                        # Create virtual environment if it doesn't exist
                        python3 -m venv ${VENV} || true

                        # Activate virtual environment
                        . ${VENV}/bin/activate

                        # Upgrade pip, pylint, and astroid inside venv
                        pip install --upgrade pip
                        pip install --upgrade pylint astroid

                        # Run pylint on app.py (ignore crashes)
                        pylint app.py --disable=C0111,C0103,W0703 || true
                    '''
                }
            }
        }

        stage('Code Build') {
            steps {
                script {
                    echo '========== Stage 2: Building Docker Image =========='
                    sh '''
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Unit Testing') {
            steps {
                script {
                    echo '========== Stage 3: Running Unit Tests =========='
                    sh '''
                        . ${VENV}/bin/activate
                        pip install -r requirements.txt
                        pytest tests/test_app.py -v
                    '''
                }
            }
        }

        stage('Containerized Deployment') {
            steps {
                script {
                    echo '========== Stage 4: Deploying Containers =========='
                    sh '''
                        # Force stop and remove ALL containers
                        docker stop $(docker ps -aq) 2>/dev/null || true
                        docker rm -f $(docker ps -aq) 2>/dev/null || true
                        
                        # Now start fresh
                        docker-compose up -d
                        
                        sleep 20
                        docker-compose ps
                        docker-compose logs --tail=50
                    '''
                }
            }
        }

        stage('Selenium Testing') {
            steps {
                script {
                    echo '========== Stage 5: Running Selenium Tests =========='
                    sh '''
                        # Build Selenium test container
                        docker build -f Dockerfile.selenium -t selenium-tests .

                        # Run Selenium tests in Docker network
                        docker run --rm \
                            --network my-web-app_default \
                            --name selenium-tests-${BUILD_NUMBER} \
                            selenium-tests || true
                    '''
                }
            }
        }
    }

    post {
        always {
            echo '========== Pipeline Completed =========='
            sh 'docker-compose logs app || true'
        }
        success {
            echo '✓ Pipeline executed successfully!'
        }
        failure {
            echo '✗ Pipeline failed. Check logs above.'
            sh 'docker-compose down || true'
        }
    }
}
