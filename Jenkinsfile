pipeline {
    agent any

    environment {
        VENV_DIR = '.venv'
        PYTHON = "${VENV_DIR}\\Scripts\\python.exe"
        PYTEST_CMD = "pytest -m e2e"
    }

    stages {

        stage('Checkout Source') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Creating fresh virtual environment & installing dependencies...'
                bat """
                    if exist %VENV_DIR% rmdir /s /q %VENV_DIR%
                    py -3.11 -m venv %VENV_DIR
                    %PYTHON% -m pip install --upgrade pip setuptools wheel
                    %PYTHON% -m pip install -r requirements.txt
                """
            }
        }

        stage('Install Playwright Browsers') {
            steps {
                echo 'Installing Playwright browsers...'
                bat """
                    %PYTHON% -m playwright install
                """
            }
        }

        stage('Run E2E Tests') {
            steps {
                echo 'Running E2E API tests...'
                bat """
                    %PYTHON% -m %PYTEST_CMD% --alluredir=allure_reports
                """
            }
        }

        stage('Publish Allure Report') {
            steps {
                echo 'Publishing Allure report...'
                allure includeProperties: false, results: [[path: 'allure_reports']]
            }
        }
    }

    post {
        always {
            echo 'Archiving logs...'
            archiveArtifacts artifacts: 'logs/*.log', allowEmptyArchive: true
        }

        success {
            echo 'API E2E pipeline SUCCESS'
        }

        failure {
            echo 'API E2E pipeline FAILED'
        }
    }
}