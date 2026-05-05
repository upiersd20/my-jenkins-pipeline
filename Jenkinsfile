pipeline {
    agent any
    
    tools {
        maven 'Maven-3'
    }
    
    stages {
        stage('Static Code Analysis') {
            steps {
                echo '🔍 Running static code analysis...'
                bat 'mvn --version'
                bat 'mvn checkstyle:checkstyle pmd:pmd'
            }
            post {
                always {
                    archiveArtifacts artifacts: '**/checkstyle-result.xml, **/pmd.xml', allowEmptyArchive: true
                }
            }
        }
        
        stage('Compile & Test') {
            steps {
                echo '🛠️ Compiling and testing...'
                bat 'mvn clean compile test'
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }
        
        stage('Package') {
            steps {
                echo '📦 Creating JAR artifact...'
                bat 'mvn package -DskipTests'
            }
        }
    }
    
    post {
        always {
            echo '📂 Archiving artifacts...'
            archiveArtifacts artifacts: '**/target/*.jar', fingerprint: true
        }
        
        success {
            echo "✅ Build SUCCESSFUL for branch: ${env.BRANCH_NAME}"
        }
        
        failure {
            echo "❌ Build FAILED! Check console output."
        }
    }
}
