pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/YOUR_GITHUB_USERNAME/sample-python-app.git',
                    branch: 'main'
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    python3 -m pip install --user flake8
                    python3 -m flake8 app tests scripts --max-line-length=120
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    python3 -m pip install --user pytest
                    python3 -m pytest tests/ -v
                '''
            }
        }

        stage('AI Code Review') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'ANTHROPIC_API_KEY',
                        variable: 'ANTHROPIC_API_KEY'
                    )
                ]) {
                    sh '''
                        python3 -m pip install --user anthropic
                        python3 scripts/ai_review.py
                    '''
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts(
                artifacts: 'ai_review_report.txt',
                allowEmptyArchive: true
            )
        }
    }
}
