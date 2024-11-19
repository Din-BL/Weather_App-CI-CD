pipeline {
    agent {
        label 'agent'
    }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        // SLACK_CREDENTIAL_ID   = credentials('Slack_Token')
        SSH_KEY               = credentials('SSH_Master-Node')
        GITHUB_CREDENTIALS    = credentials('GitHub_PAT')
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

        stage('Retrieve Git Tag') {
            steps {
                script {
                    echo 'Retrieving Git Tag...'
                    def gitTag = sh(script: "git describe --tags", returnStdout: true).trim()
                    echo "Git Tag: ${gitTag}"
                    env.IMAGE_TAG = gitTag // Save Git tag as environment variable
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
                    sh "sudo docker build -t dinbl/weather_app:${env.IMAGE_TAG} ."
                    sh "sudo docker tag dinbl/weather_app:${env.IMAGE_TAG} dinbl/weather_app:latest"
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

                echo 'Updating Helm Chart in GitHub Repository...'
                sh """
                        git clone https://${GITHUB_CREDENTIALS}@github.com/Din-BL/Helm-Charts.git
                        cd Helm-Charts
                        sed -i 's/tag: .*/tag: ${env.IMAGE_TAG}/g' values.yaml
                        git config user.name "Din"
                        git config user.email "Dinz5005@gmail.com"
                        git add .
                        git commit -m "Update Docker image tag to ${env.IMAGE_TAG}"
                        git push https://${GITHUB_CREDENTIALS}@github.com/Din-BL/Helm-Charts.git main
                    """

                // slackSend(
                //     channel: '#cicd-project',
                //     message: "Pipeline completed successfully. Image tag: ${env.IMAGE_TAG}",
                //     tokenCredentialId: SLACK_CREDENTIAL_ID
                // )
            }
        }
        failure {
            script {
                echo 'Pipeline failed'
                // slackSend(
                //     channel: '#cicd-project',
                //     message: 'Pipeline failed.',
                //     tokenCredentialId: SLACK_CREDENTIAL_ID
                // )
            }
        }
    }
}
