pipeline {
    agent { label 'agent' }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        SLACK_CREDENTIAL_ID = 'Slack_Token'
        SSH_KEY = credentials('SSH_Master-Node')
    }
    stages {
        stage('Clean') {
            steps {
                script {
                    echo 'Cleaning up old Docker containers and images'
                    sh """
                    sudo docker stop weather_app || true
                    sudo docker rm weather_app || true
                    sudo docker rmi dinbl/weather_app:latest || true
                    """
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Testing...'
                    sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    # Run tests
                    python3 test_app.py
                    """
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    echo "Fetching all updates from the Git repository..."
                    sh """
                    git fetch --tags --force
                    git fetch origin +refs/heads/*:refs/remotes/origin/*
                    git reset --hard origin/main
                    """

                    echo "Retrieving the latest Git tag..."
                    def gitTag = sh(script: "git describe --tags --abbrev=0", returnStdout: true).trim()
                    if (!gitTag) {
                        error "No Git tag found. Ensure tags are created and pushed to the repository."
                    }
                    env.IMAGE_TAG = gitTag // Set as environment variable for use in later stages

                    echo "Building Docker image with tag: ${env.IMAGE_TAG}"
                    sh """
                    sudo docker build --no-cache -t dinbl/weather_app:${env.IMAGE_TAG} .
                    """
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing Docker image with tag: ${env.IMAGE_TAG}"
                    sh """
                    echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u dinbl --password-stdin
                    sudo docker push dinbl/weather_app:${env.IMAGE_TAG}
                    sudo docker tag dinbl/weather_app:${env.IMAGE_TAG} dinbl/weather_app:latest
                    sudo docker push dinbl/weather_app:latest
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs() // Clean up the workspace
        }
        success {
            agent { label 'master' }
            script {
                echo "Deployment complete. Image tag: ${env.IMAGE_TAG}"
                slackSend(channel: '#cicd-project',
                          message: "Pipeline completed successfully. Docker image tag: ${env.IMAGE_TAG}",
                          tokenCredentialId: SLACK_CREDENTIAL_ID)
            }
        }
        failure {
            agent { label 'master' }
            script {
                echo 'Pipeline failed'
                slackSend(channel: '#cicd-project',
                          message: 'Pipeline failed.',
                          tokenCredentialId: SLACK_CREDENTIAL_ID)
            }
        }
    }
}
