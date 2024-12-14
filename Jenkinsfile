pipeline {
    agent any
    stages {
        stage('Debug Environment') {
            steps {
                script {
                    echo "Available environment variables:"
                    sh 'env | sort'
                }
            }
        }
        stage('Branch Check') {
            steps {
                script {
                    // נסה להשתמש ב-BRANCH_NAME או GIT_BRANCH
                    def branchName = env.BRANCH_NAME ?: env.GIT_BRANCH

                    if (branchName == null || branchName.isEmpty()) {
                        echo 'Branch name is not defined!'
                        error 'Pipeline cannot continue without a branch name.'
                    } else if (branchName == 'main' || branchName == 'origin/main') {
                        echo 'You are on the main branch!'
                    } else if (branchName.startsWith('feature/') || branchName.startsWith('origin/feature/')) {
                        echo 'You are on a feature branch!'
                    } else {
                        echo "You are on branch: ${branchName}"
                    }
                }
            }
        }
    }
}
