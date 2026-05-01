pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTEST_CMD = 'pytest -m e2e'
    }

    options {
        timeout(time: 40, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
            }
        }

        stage('Create Python 3.11 Environment') {
            steps {
                echo '🐍 Creating virtual environment...'
                bat """
                    py -3.11 -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Installing dependencies...'
                bat """
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pip install -r requirements.txt
                """
            }
        }

        stage('Install Playwright Browsers') {
            steps {
                echo '🌐 Installing Playwright browsers...'
                bat """
                    call %VENV_DIR%\\Scripts\\activate.bat
                    playwright install
                """
            }
        }

        stage('Run E2E Tests') {
            steps {
                echo '🧪 Running E2E tests...'
                bat """
                    call %VENV_DIR%\\Scripts\\activate.bat
                    %PYTEST_CMD% --alluredir=allure-results
                """
            }

            post {
                always {
                    archiveArtifacts artifacts: 'logs/*.log', allowEmptyArchive: true
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                echo '📊 Publishing Allure report...'
                allure includeProperties: false, results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning workspace...'
            bat "if exist %VENV_DIR% rmdir /s /q %VENV_DIR%"
        }

        success {
            echo '✅ E2E pipeline SUCCESS'
        }

        failure {
            echo '❌ E2E pipeline FAILED'
        }
    }
}