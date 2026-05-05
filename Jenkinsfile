pipeline {
    agent any
    
    stages {
        stage('Static Code Analysis') {
            steps {
                echo '🔍 Running static code analysis...'
                // Проверяем версию Maven
                sh 'mvn --version'
                // Запускаем анализ (если нет pom.xml с плагинами, просто выведем предупреждение)
                sh 'mvn checkstyle:checkstyle pmd:pmd || echo "Анализ пропущен - плагины не настроены"'
            }
            post {
                always {
                    // Публикуем отчёты, если они есть
                    recordIssues enabledForFailure: true, tools: [
                        checkStyle(pattern: '**/checkstyle-result.xml'),
                        pmd(pattern: '**/pmd.xml')
                    ]
                }
            }
        }
        
        stage('Compile & Test') {
            steps {
                echo '🛠️ Compiling and testing...'
                sh 'mvn clean compile test'
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
                sh 'mvn package -DskipTests'
            }
        }
    }
    
    post {
        always {
            echo '📂 Archiving artifacts...'
            // Сохраняем JAR файлы и отчёты
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
