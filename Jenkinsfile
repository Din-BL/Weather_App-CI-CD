pipeline {
    agent { label 'aws-dynamic-agent' }  

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        GITHUB_TOKEN          = credentials('GitHub_PAT')
        SLACK_TOKEN           = credentials('Slack_Token')
        SONARQUBE_URL         = credentials('SonarQube_URL')
        SONARQUBE_TOKEN       = credentials('SonarQube-Token')
    }
    
    stages {

        stage('Retrieve Latest Git Tag') {
            when {
                branch 'main'
            }
            steps {
                echo 'Fetching the latest Git Tag...'
                script {
                    sh 'git fetch --tags --depth=1'
                    env.IMAGE_TAG = sh(script: "git describe --tags --abbrev=0", returnStdout: true).trim()
                    echo "Latest Git Tag: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Parallel Tasks') {
            parallel {
                stage('SonarQube Analysis') {
                    steps {
                        echo 'Running SonarQube analysis...'
                        withSonarQubeEnv('SonarQube') { 
                            sh """
                            /opt/sonar-scanner/bin/sonar-scanner \
                                -Dsonar.projectKey=CI-CD-Weather_App \
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
            }
        }

        stage('Build') {
            when {
                branch 'main'
            }
            steps {
                echo 'Building Docker image...'
                sh """
                sudo docker build -t dinbl/weather_app:${env.IMAGE_TAG} .
                sudo docker tag dinbl/weather_app:${env.IMAGE_TAG} dinbl/weather_app:latest
                """
            }
        }

        stage('Push to Docker Hub') {
            when {
                branch 'main'
            }
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
        success {
            script {
                echo 'Pipeline completed successfully.'
                if (env.BRANCH_NAME != null && !env.BRANCH_NAME.startsWith('feature')) {
                    updateHelmChart(env.IMAGE_TAG)
                    sendSlackNotification("Pipeline completed successfully. Image tag: ${env.IMAGE_TAG}")
                } else {
                    sendSlackNotification("Pipeline completed successfully.")
                }
            }
        }

        failure {
            script {
                echo 'Pipeline failed.'
                if (env.BRANCH_NAME != null && !env.BRANCH_NAME.startsWith('feature')) {
                    sendSlackNotification("Pipeline failed. Image tag: ${env.IMAGE_TAG}")
                } else {
                    sendSlackNotification("Pipeline failed.")
                }
            }
        }
    }
}

def updateHelmChart(imageTag) {
    withCredentials([string(credentialsId: 'GitHub_PAT', variable: 'GIT_TOKEN')]) {
        sh """
        if [ ! -d Helm-Charts ]; then
            git clone https://${GIT_TOKEN}@github.com/Din-BL/Helm-Charts.git
        else
            cd Helm-Charts
            git reset --hard
            git pull origin main
            cd ..
        fi

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
