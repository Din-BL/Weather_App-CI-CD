pipeline {
    agent any
    stages {
        stage('Branch Check') {
            steps {
                script {
                    // בדיקה אם BRANCH_NAME מוגדר, אחרת להשתמש ב-GIT_BRANCH
                    def branchName = env.BRANCH_NAME ?: env.GIT_BRANCH

                    if (branchName == null || branchName.isEmpty()) {
                        echo 'Branch name is not defined!'
                        error 'Pipeline cannot continue without a branch name.'
                    } else if (branchName == 'main') {
                        echo 'You are on the main branch!'
                    } else if (branchName.startsWith('feature/')) {
                        echo 'You are on a feature branch!'
                    } else {
                        echo "You are on branch: ${branchName}"
                    }
                }
            }
        }
    }
}
