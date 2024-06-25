pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'http://172.31.52.252/root/weather_app.git'
            }
        }
        stage('Build') {
            steps {
                // Add your build steps here
                echo 'Building...'
                // For example, if you use Maven, you could use:
                // sh 'mvn clean install'
            }
        }
        stage('Test') {
            steps {
                // Add your test steps here
                echo 'Testing...'
                // For example, if you use JUnit, you could use:
                // junit 'target/surefire-reports/*.xml'
            }
        }
        stage('Deploy') {
            steps {
                // Add your deploy steps here
                echo 'Deploying...'
                // For example, you could use:
                // sh 'scp -r * user@your.server:/path/to/deploy'
            }
        }
    }
}

