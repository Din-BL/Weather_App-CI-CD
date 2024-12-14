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
                    // שימוש במשתנה branchName עם ברירת מחדל
                    def branchName = env.BRANCH_NAME ?: env.GIT_BRANCH ?: 'unknown'

                    if (branchName == 'unknown') {
                        echo 'Branch name is not defined!'
                        error 'Pipeline cannot proceed without a branch name.'
                    } else if (branchName.contains('main')) {
                        echo 'You are on the main branch!'
                    } else if (branchName.contains('feature/')) {
                        echo 'You are on a feature branch!'
                    } else {
                        echo "You are on branch: ${branchName}"
                    }
                }
            }
        }
    }
    post {
        always {
            echo 'Cleaning workspace...'
            cleanWs() // מחיקת כל הקבצים מה-Workspace
        }
    }
}
