pipeline {
    agent any
    
    stages {
        stage('Static Analysis') {
            steps {
                echo 'Running static code analysis...'
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building project...'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline finished!'
            archiveArtifacts artifacts: '**/*', fingerprint: true
        }
    }
}
