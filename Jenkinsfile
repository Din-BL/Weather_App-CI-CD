pipeline {
    agent { label 'agent' }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials') // Using your Docker Hub credentials ID
        SLACK_CREDENTIAL_ID = 'Slack_Token' 
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'http://172.31.52.252/root/weather_app.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    echo 'Building...'
                    sh 'sudo docker build -t weather_app .'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    echo 'Testing...'
                    // Uncomment the next line to run tests inside the Docker container
                    // sh 'docker run --rm weather_app pytest'
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo 'Pushing to Docker Hub...'
                    sh """
                    echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u dinbl --password-stdin
                    sudo docker tag weather_app dinbl/weather_app:latest
                    sudo docker push dinbl/weather_app:latest
                    """
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying...'
                    sh 'sudo docker run --name weather_app -d -p 5000:5000 weather_app'
                }
            }
        }
    }
    post {
        success {
            script {
                echo 'Pipeline completed successfully.'
            }
            slackSend (channel: '#cicd-project', message: 'Pipeline completed successfully.', tokenCredentialId: SLACK_CREDENTIAL_ID)
        }
        failure {
            script {
                echo 'Pipeline failed.'
            }
            slackSend (channel: '#cicd-project', message: 'Pipeline failed.', tokenCredentialId: SLACK_CREDENTIAL_ID)
        }
    }
}
