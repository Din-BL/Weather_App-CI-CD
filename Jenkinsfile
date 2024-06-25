pipeline {
    // Specify that the pipeline can run on any available agent
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the Git repository using the specified credentials and branch
                git credentialsId: 'glft-ifR1jMBbTALeMqyWkzdP', url: 'http://172.31.52.252/root/weather_app.git', branch: 'main'
            }
        }
    }

    post {
        always {
            // Clean the workspace after the build, regardless of the result (success, failure, or aborted)
            cleanWs()
        }
    }
}
