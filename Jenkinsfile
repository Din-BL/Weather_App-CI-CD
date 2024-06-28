pipeline {
    agent { label 'agent' }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        SLACK_CREDENTIAL_ID = 'Slack_Token'
        SSH_KEY = credentials('SSH_Key') // Make sure this matches the ID of your SSH key credentials
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'http://172.31.52.252/root/weather_app.git'
            }
        }
        stage('Clean') {
            steps {
                script {
                    echo 'Cleaning up old Docker containers and images...'
                    sh """
                    # Stop and remove the old container if it exists
                    if sudo docker ps -a | grep weather_app; then
                        sudo docker stop weather_app || true
                        sudo docker rm weather_app || true
                    fi
                    # Remove all old images, including dangling images
                    sudo docker image prune -af || true
                    """
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
        stage('Build') {
            steps {
                script {
                    echo 'Building...'
                    sh 'sudo docker build -t weather_app .'
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
                    sh """
                    sudo docker run --name weather_app -d -p 5000:5000 dinbl/weather_app:latest
                    """
                }
            }
        }
    }
    post {
        always {
            agent { label 'master' }
            script {
                echo 'Running post actions on master node...'
                echo 'Debugging Information:'
                echo 'Environment Variables:'
                sh 'printenv'
            }
        }
        success {
            agent { label 'master' }
            script {
                echo 'Pipeline completed successfully.'
                echo 'Debugging Information:'
                echo "Using SSH Key ID: ${SSH_KEY}"
                echo 'Environment Variables:'
                sh 'printenv'
                sh """
                echo "${SSH_KEY}" > /tmp/ssh_key
                chmod 600 /tmp/ssh_key
                ssh -i /tmp/ssh_key -o StrictHostKeyChecking=no ec2-user@172.31.22.33 "bash /home/ec2-user/production/image_script.sh"
                rm -f /tmp/ssh_key
                """
                slackSend (channel: '#cicd-project', message: 'Pipeline completed successfully.', tokenCredentialId: SLACK_CREDENTIAL_ID)
            }
        }
        failure {
            agent { label 'master' }
            script {
                echo 'Pipeline failed.'
                echo 'Debugging Information:'
                echo "Using SSH Key ID: ${SSH_KEY}"
                echo 'Environment Variables:'
                sh 'printenv'
                slackSend (channel: '#cicd-project', message: 'Pipeline failed.', tokenCredentialId: SLACK_CREDENTIAL_ID)
            }
        }
    }
}

