pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.12'
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat """
                    python -m venv ${VENV_DIR}
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements_updated.txt
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    pip install -r requirements_updated.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running API tests...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    pytest tests/ --allure-dir=allure-results --junitxml=test-results.xml
                """
            }
            post {
                always {
                    echo 'Archiving test results...'
                    junit 'test-results.xml'
                    archiveArtifacts artifacts: 'logs/*.log', allowEmptyArchive: true
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Generating Allure report...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    allure generate allure-results --clean
                """
            }
            post {
                always {
                    allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed. Cleaning up...'
            bat """
                if exist ${VENV_DIR} rmdir /s /q ${VENV_DIR}
                if exist allure-results rmdir /s /q allure-results
            """
        }
        success {
            echo '✅ All tests passed!'
            emailext (
                subject: "✅ Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Good news! The API tests have passed successfully.\n\nBuild: ${env.BUILD_URL}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
        failure {
            echo '❌ Tests failed!'
            emailext (
                subject: "❌ Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "The API tests have failed. Please check the logs.\n\nBuild: ${env.BUILD_URL}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
}
