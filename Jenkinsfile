pipeline {
    agent any
    stages {
        stage('Debug Environment') {
            steps {
                script {
                    echo "Listing all environment variables:"
                    sh 'env | sort'
                }
            }
        }
        stage('Branch Check') {
            steps {
                script {
                    // שימוש בברירת מחדל אם BRANCH_NAME ריק
                    def branchName = env.BRANCH_NAME ?: env.GIT_BRANCH ?: 'unknown'

                    if (branchName == 'unknown') {
                        echo 'Branch name is not available.'
                        error 'Pipeline cannot proceed without a branch name.'
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
