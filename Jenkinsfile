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
                    sh "sudo docker run --name weather_app -d -p 5000:5000 dinbl/weather_app:${env.IMAGE_TAG}"
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
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            agent { label 'master' }
            script {
                echo 'Deploy'
                slackSend(channel: '#cicd-project', message: "Pipeline completed successfully. Image tag: ${env.IMAGE_TAG}", tokenCredentialId: SLACK_CREDENTIAL_ID)
            }
        }
        failure {
            agent { label 'master' }
            script {
                echo 'Pipeline failed'
                slackSend(channel: '#cicd-project', message: 'Pipeline failed.', tokenCredentialId: SLACK_CREDENTIAL_ID)
            }
        }
    }
}
