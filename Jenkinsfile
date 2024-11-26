pipeline {
    agent {
        label 'agent'
    }

    environment {
        SLACK_CREDENTIAL_ID   = credentials('Slack_Token')
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        SSH_KEY               = credentials('SSH_Master-Node')
        GITHUB_TOKEN          = credentials('GitHub_PAT') 
    }

    stages {
        stage('Clean') {
            steps {
                script {
                    echo 'Cleaning up all Docker containers and images'
                    sh """
                    # Stop and remove all running containers
                    sudo docker ps -aq | xargs -r sudo docker stop
                    sudo docker ps -aq | xargs -r sudo docker rm

                    # Remove all Docker images
                    sudo docker images -aq | xargs -r sudo docker rmi -f
                    """
                }
            }
        }

        stage('Retrieve Git Tag') {
            steps {
                script {
                    echo 'Retrieving Git Tag...'
                    def gitTag = sh(script: "git describe --tags", returnStdout: true).trim()
                    echo "Git Tag: ${gitTag}"
                    env.IMAGE_TAG = gitTag 
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
                    echo 'Building...'
                    sh """
                    sudo docker build -t dinbl/weather_app:${env.IMAGE_TAG} .
                    sudo docker tag dinbl/weather_app:${env.IMAGE_TAG} dinbl/weather_app:latest
                    """
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo 'Pushing to Docker Hub'
                    sh """
                    echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u dinbl --password-stdin
                    sudo docker push dinbl/weather_app:${env.IMAGE_TAG}
                    sudo docker push dinbl/weather_app:latest
                    """
                }
            }
        }
    }

    post {
        always {
            script {
                node {
                    cleanWs()
                }
            }
        }

        success {
            script {
                echo 'Pipeline completed successfully. Updating resources...'

                withCredentials([string(credentialsId: 'GitHub_PAT', variable: 'GIT_TOKEN')]) {
                    sh """
                    # Clone the Helm chart repo or pull the latest changes
                    if [ ! -d Helm-Charts ]; then
                        git clone https://${GIT_TOKEN}@github.com/Din-BL/Helm-Charts.git
                    else
                        cd Helm-Charts
                        git reset --hard  # Ensure clean working directory
                        git pull origin main
                        cd ..
                    fi

                    # Update the Docker image tag in the Helm chart
                    cd Helm-Charts
                    sed -i 's/tag: .*/tag: ${env.IMAGE_TAG}/g' values.yaml
                    git config user.name "Din"
                    git config user.email "Dinz5005@gmail.com"
                    git add .
                    git commit -m "Update Docker image tag to ${env.IMAGE_TAG}"
                    git push https://${GIT_TOKEN}@github.com/Din-BL/Helm-Charts.git main
                    """
                }

                slackSend(
                    channel: '#cicd-project',
                    message: "Pipeline completed successfully. Image tag: ${env.IMAGE_TAG}",
                    tokenCredentialId: SLACK_CREDENTIAL_ID
                    echo "SLACK_CREDENTIAL_ID: ${SLACK_CREDENTIAL_ID}"
                    echo "SLACK_CREDENTIAL_ID: ${Slack_Token}"
                )
            }
        }

        failure {
            script {
                echo 'Pipeline failed'
                slackSend(
                    channel: '#cicd-project',
                    message: 'Pipeline failed.',
                    tokenCredentialId: SLACK_CREDENTIAL_ID
                    echo "SLACK_CREDENTIAL_ID: ${SLACK_CREDENTIAL_ID}"
                    echo "SLACK_CREDENTIAL_ID: ${Slack_Token}"
                )
            }
        }
    }
}
