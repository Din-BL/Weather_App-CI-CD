pipeline {
    agent {
        label 'agent'
    }

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        SSH_KEY               = credentials('SSH_Master-Node')
        GITHUB_TOKEN          = credentials('GitHub_PAT')
        SLACK_TOKEN           = credentials('Slack_Token')
        SONARQUBE_URL         = 'http://10.0.11.210:9000'
        SONARQUBE_TOKEN       = credentials('Sonar_Token')
    }

    stages {
        stage('Clean') {
            steps {
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

        stage('Retrieve Git Tag') {
            steps {
                echo 'Retrieving Git Tag...'
                script {
                    env.IMAGE_TAG = sh(script: "git describe --tags", returnStdout: true).trim()
                    echo "Git Tag: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                withSonarQubeEnv('SonarQube') { 
                    sh """
                    /opt/sonar-scanner/bin/sonar-scanner \
                        -Dsonar.projectKey=WeatherApp \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=${SONARQUBE_URL} \
                        -Dsonar.token=${SONARQUBE_TOKEN}
                    """
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh """
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                python3 test_app.py
                """
            }
        }

        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh """
                sudo docker build -t dinbl/weather_app:${env.IMAGE_TAG} .
                sudo docker tag dinbl/weather_app:${env.IMAGE_TAG} dinbl/weather_app:latest
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                sh """
                echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u dinbl --password-stdin
                sudo docker push dinbl/weather_app:${env.IMAGE_TAG}
                sudo docker push dinbl/weather_app:latest
                """
            }
        }
    }

    post {
        always {
            cleanWs()
        }

        success {
            echo 'Pipeline completed successfully. Updating resources...'
            updateHelmChart(env.IMAGE_TAG)
            sendSlackNotification("Pipeline completed successfully. Image tag: ${env.IMAGE_TAG}")
        }

        failure {
            echo 'Pipeline failed.'
            sendSlackNotification("Pipeline failed. Image tag: ${env.IMAGE_TAG}")
        }
    }
}

def updateHelmChart(imageTag) {
    withCredentials([string(credentialsId: 'GitHub_PAT', variable: 'GIT_TOKEN')]) {
        sh """
        # Clone the Helm chart repo or pull the latest changes
        if [ ! -d Helm-Charts ]; then
            git clone https://${GIT_TOKEN}@github.com/Din-BL/Helm-Charts.git
        else
            cd Helm-Charts
            git reset --hard
            git pull origin main
            cd ..
        fi

        # Update the Docker image tag in the Helm chart
        cd Helm-Charts
        sed -i 's/tag: .*/tag: ${imageTag}/g' values.yaml
        git config user.name "Din"
        git config user.email "Dinz5005@gmail.com"
        git add .
        git commit -m "Update Docker image tag to ${imageTag}"
        git push https://${GIT_TOKEN}@github.com/Din-BL/Helm-Charts.git main
        """
    }
}

def sendSlackNotification(message) {
    withCredentials([string(credentialsId: 'Slack_Token', variable: 'SLACK_TOKEN')]) {
        slackSend(
            channel: '#cicd-project',
            message: message,
            token: SLACK_TOKEN
        )
    }
}
