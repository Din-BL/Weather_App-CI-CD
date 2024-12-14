pipeline {
    agent any
    stages {
        stage('Testing') {
            when {
                branch 'feature/*'
            }
            steps {
                echo "Running tests on a feature branch..."
                // Add your testing commands here
            }
        }
        stage('Build') {
            when {
                branch 'main'
            }
            steps {
                echo "Building on main branch..."
                // Add your build commands here
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo "Deploying on main branch..."
                // Add your deploy commands here
            }
        }
    }
}
