pipeline {
    agent any
    stages {
        stage('Debug Environment') {
            steps {
                script {
                    echo "Debugging environment variables..."
                    echo "BRANCH_NAME: ${env.BRANCH_NAME}"
                    echo "GIT_BRANCH: ${env.GIT_BRANCH}"
                    echo "GIT_COMMIT: ${env.GIT_COMMIT}"
                }
            }
        }
        stage('Branch Check') {
            steps {
                script {
                    def branchName = env.BRANCH_NAME ?: env.GIT_BRANCH

                    if (branchName == null || branchName.isEmpty()) {
                        echo 'Branch name is not defined!'
                        error 'Pipeline cannot continue without a branch name.'
                    } else if (branchName == 'main') {
                        echo 'You are on the main branch!'
                    } else if (branchName.startsWith('origin/feature/')) {
                        echo 'You are on a feature branch!'
                    } else {
                        echo "You are on branch: ${branchName}"
                    }
                }
            }
        }
    }
}
