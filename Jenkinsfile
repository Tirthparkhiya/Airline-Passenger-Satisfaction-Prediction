pipeline {
    agent any
    
    environment {
        VENV_DIR='venv'
    }

    stages {
        stage('Cloning from Github Repo') {
            steps {
                script {
                    //Cloning
                    echo 'Cloning from Github Repo.......'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-github-token', url: 'https://github.com/Tirthparkhiya/Airline-Passenger-Satisfaction-Prediction.git']])
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    //Setup Virtual Environment
                    echo 'Setup Virtual Environment.......'
                    sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }

        stage('Linting Code') {
            steps {
                script {
                    //Linting Code
                    echo 'Linting Code......'
                    sh '''
                        set -e
                        . ${VENV_DIR}/bin/activate
                        pylint app.py main.py --output=pylint-report.txt --exit-zero || echo "pylint stage completed"
                        flake8 app.py main.py --ignore=E501,E302 --output-file=flake8-report.txt || echo "flake8 stage completed"
                        black app.py main.py || echo "Black stage completed"


                    '''
                }
            }
        }

        stage('Trivy Scanning') {
            steps {
                script {
                    //Trivy Scanning
                    echo 'Trivy Scanning.......'
                    sh "trivy fs ./ --format table -o trivy-fs-report.html"

                }
            }
        }
    }
}