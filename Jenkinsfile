pipeline {
    agent any
    
    tools {
        maven 'Maven-3.8.1'   // Убедитесь, что название совпадает с Jenkins → Tools
        jdk 'JDK-11'          // Убедитесь, что название совпадает с Jenkins → Tools
    }

    stages {
        // Этап 1: Статический анализ кода
        stage('Static Code Analysis') {
            steps {
                echo '🔍 Running static code analysis...'
                sh 'mvn clean compile checkstyle:checkstyle pmd:pmd spotbugs:spotbugs'
            }
            post {
                always {
                    // Публикуем отчёты в Jenkins UI
                    recordIssues tools: [
                        checkStyle(pattern: '**/checkstyle-result.xml'),
                        pmd(pattern: '**/pmd.xml'),
                        spotBugs(pattern: '**/spotbugsXml.xml')
                    ]
                    // Сохраняем отчёты как артефакты
                    archiveArtifacts artifacts: '**/checkstyle-result.xml, **/pmd.xml, **/spotbugsXml.xml', fingerprint: true
                }
            }
        }
        
        // Этап 2: Компиляция и тесты
        stage('Compile & Test') {
            steps {
                echo '🛠️ Compiling and running tests...'
                sh 'mvn clean test-compile'
                sh 'mvn test'
            }
            post {
                always {
                    // Публикуем результаты тестов
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }
        
        // Этап 3: Упаковка (создание JAR)
        stage('Package') {
            steps {
                echo '📦 Packaging application...'
                sh 'mvn package -DskipTests'
            }
        }
    }
    
    post {
        // Всегда выполняется (успех или провал)
        always {
            echo '📂 Archiving artifacts...'
            // Сохраняем JAR файлы в бинарном репозитории Jenkins
            archiveArtifacts artifacts: '**/target/*.jar', fingerprint: true
            
            // Выводим информацию о сборке
            echo """
            ====================================
            Job: ${env.JOB_NAME}
            Build: ${env.BUILD_NUMBER}
            Branch: ${env.BRANCH_NAME}
            Status: ${currentBuild.currentResult}
            URL: ${env.BUILD_URL}
            ====================================
            """
        }
        
        // При успешной сборке - разная логика для разных веток
        success {
            script {
                if (env.BRANCH_NAME == 'main') {
                    echo """
                    🎉✅ MAIN BRANCH - PRODUCTION BUILD SUCCESSFUL ✅🎉
                    
                    Артефакт готов к деплою на production!
                    JAR файл сохранён в Jenkins артефактах.
                    """
                } 
                else if (env.BRANCH_NAME == 'develop') {
                    echo """
                    🔄✅ DEVELOP BRANCH - INTEGRATION BUILD SUCCESSFUL ✅🔄
                    
                    Интеграционная сборка проверена.
                    Можете сливать в main после code review.
                    """
                } 
                else if (env.BRANCH_NAME.startsWith('feature/')) {
                    echo """
                    🌿✅ FEATURE BRANCH - CHECK PASSED ✅🌿
                    
                    Функциональная ветка: ${env.BRANCH_NAME}
                    Статический анализ и тесты пройдены.
                    """
                }
                else {
                    echo "✅ Build successful for branch: ${env.BRANCH_NAME}"
                }
            }
        }
        
        // При провале сборки
        failure {
            echo """
            ❌❌❌ PIPELINE FAILED ❌❌❌
            
            Branch: ${env.BRANCH_NAME}
            Check logs: ${env.BUILD_URL}/console
            
            Возможные причины:
            - Ошибки компиляции
            - Падающие тесты
            - Нарушения Checkstyle/PMD/SpotBugs
            """
        }
        
        // При нестабильной сборке (например, упали некоторые тесты)
        unstable {
            echo "⚠️ Unstable build! Some tests failed. Check test reports."
        }
    }
}
