pipeline {
    agent { label 'agent' }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        SLACK_CREDENTIAL_ID = 'Slack_Token'
        SSH_KEY = credentials('SSH_Key') 
    }
    stages {
        stage('Clean') {
            steps {
                script {
                    echo 'Cleaning up old Docker containers and images'
                    sh """
                    # Stop and remove the old container if it exists
                    if sudo docker ps -a | grep weather_app; then
                        sudo docker stop weather_app
                        sudo docker rm weather_app
                    fi
                    # Remove old image
                    sudo docker rmi dinbl/weather_app:latest
                    """
                }
            }
        }
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'http://172.31.52.252/root/weather_app.git'
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
        stage('Build') {
            steps {
                script {
                    echo 'Building...'
                    sh 'sudo docker build -t dinbl/weather_app:latest .'
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo 'Pushing to Docker Hub...'
                    sh """
                    echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u dinbl --password-stdin
                    sudo docker push dinbl/weather_app:latest
                    """
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying...'
                    sh """
                    sudo docker run --name weather_app -d -p 5000:5000 dinbl/weather_app:latest
                    """
                }
            }
        }
    }
    post {
        success {
            agent { label 'master' }
            withCredentials([sshUserPrivateKey(credentialsId: 'SSH_Key', keyFileVariable: 'SSH_KEY_FILE')]) {
                script {
                    echo 'Pipeline completed successfully.'
                    sh """
                    ssh -i $SSH_KEY_FILE -o StrictHostKeyChecking=no ec2-user@172.31.22.33 "bash /home/ec2-user/production/image_script.sh"
                    """
                    slackSend (channel: '#cicd-project', message: 'Pipeline completed successfully.', tokenCredentialId: SLACK_CREDENTIAL_ID)
                }
            }
        }
        failure {
            agent { label 'master' }
            script {
                echo 'Pipeline failed.'
                slackSend (channel: '#cicd-project', message: 'Pipeline failed.', tokenCredentialId: SLACK_CREDENTIAL_ID)
            }
        }
    }
}

