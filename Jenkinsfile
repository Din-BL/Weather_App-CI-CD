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
                    # Stop and remove the old container
                    sudo docker stop weather_app || true
                    sudo docker rm weather_app || true
                    # Remove old image
                    sudo docker rmi dinbl/weather_app:latest || true
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
                 echo 'Testing'
                 sh """
                 python3 -m venv venv
                 if [ -d "venv" ]; then
                    echo "Virtual environment created successfully."
                    else
                        echo "Failed to create virtual environment."
                        exit 1
                 fi

                . venv/bin/activate
                if [ -f "./venv/bin/pip" ]; then
                    echo "Pip found in virtual environment."
                else
                    echo "Pip not found in virtual environment."
                    exit 1
                fi

                ./venv/bin/pip install --upgrade pip
                if [ $? -ne 0 ]; then
                    echo "Failed to upgrade pip."
                    exit 1
                fi
                ./venv/bin/pip install -r requirements.txt
                 if [ $? -ne 0 ]; then
                    echo "Failed to install requirements."
                    exit 1
                fi

            # Run tests
                ./venv/bin/python3 test_app.py
                if [ $? -ne 0 ]; then
                    echo "Tests failed."
                    exit 1
                fi
                """
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

