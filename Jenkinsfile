pipeline {
    agent any
    stages {
        stage('Branch Check') {
            steps {
                script {
                    if (env.BRANCH_NAME == null || env.BRANCH_NAME.isEmpty()) {
                        echo 'Branch name is not defined!'
                        error 'Pipeline cannot continue without a branch name.'
                    } else if (env.BRANCH_NAME == 'main') {
                        echo 'You are on the main branch!'
                    } else if (env.BRANCH_NAME.startsWith('feature/')) {
                        echo 'You are on a feature branch!'
                    } else {
                        echo "You are on branch: ${env.BRANCH_NAME}"
                    }
                }
            }
        }
    }
}
