pipeline {
    agent any
    
    stages {
        stage('Static Code Analysis') {
            steps {
                echo '🔍 Running static code analysis...'
                // Для Windows используем bat вместо sh
                bat 'mvn --version'
                bat 'mvn checkstyle:checkstyle pmd:pmd || echo "Анализ пропущен - плагины не настроены"'
            }
            post {
                always {
                    // Убираем recordIssues, так как нет плагина
                    // Просто архивируем отчёты
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
            archiveArtifacts artifacts: '**/target/*.xml', allowEmptyArchive: true
        }
        
        success {
            echo "✅ Build SUCCESSFUL for branch: ${env.BRANCH_NAME}"
        }
        
        failure {
            echo "❌ Build FAILED! Check console output."
        }
    }
}
