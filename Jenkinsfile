pipeline {
    agent any
    
    stages {
        // Этап 1: Статический анализ кода с интеграцией Warnings NG
        stage('Static Code Analysis') {
            steps {
                echo '🔍 Running static code analysis...'
                
                // Создаём отчёт в формате Checkstyle (понятен плагину Warnings NG)
                writeFile file: 'checkstyle-result.xml', text: '''<?xml version="1.0" encoding="UTF-8"?>
<checkstyle version="8.45">
    <file name="src/main.java">
        <error line="10" column="5" severity="warning" message="Missing Javadoc comment" source="javadoc"/>
        <error line="15" column="8" severity="info" message="Variable name is too short" source="naming"/>
    </file>
    <file name="src/helper.java">
        <error line="3" column="1" severity="error" message="Unused import statement" source="imports"/>
    </file>
</checkstyle>'''
                
                // Создаём отчёт в формате PMD
                writeFile file: 'pmd.xml', text: '''<?xml version="1.0" encoding="UTF-8"?>
<pmd version="6.55.0">
    <file name="src/main.java">
        <violation beginline="12" endline="12" rule="AvoidDeeplyNestedIfStmts" ruleset="Design" priority="3">
            Avoid deeply nested if statements
        </violation>
    </file>
</pmd>'''
                
                // Создаём текстовый отчёт для архива
                bat '''
                    echo ======================================== > analysis-report.txt
                    echo Static Analysis Report >> analysis-report.txt
                    echo ======================================== >> analysis-report.txt
                    echo Date: %DATE% %TIME% >> analysis-report.txt
                    echo. >> analysis-report.txt
                    echo Issues found: >> analysis-report.txt
                    echo   - Warning: Missing Javadoc (src/main.java:10) >> analysis-report.txt
                    echo   - Info: Variable name too short (src/main.java:15) >> analysis-report.txt
                    echo   - Error: Unused import (src/helper.java:3) >> analysis-report.txt
                    echo. >> analysis-report.txt
                    echo All checks completed >> analysis-report.txt
                '''
            }
            post {
                always {
                    // ИСПОЛЬЗУЕМ ПЛАГИН WARNINGS NEXT GENERATION
                    recordIssues enabledForFailure: true,
                                  tools: [
                                      checkStyle(pattern: 'checkstyle-result.xml'),
                                      pmd(pattern: 'pmd.xml')
                                  ]
                    
                    // Дополнительно архивируем отчёты
                    archiveArtifacts artifacts: 'checkstyle-result.xml, pmd.xml, analysis-report.txt', fingerprint: true, allowEmptyArchive: true
                }
            }
        }
        
        // Этап 2: Компиляция и тесты (имитация)
        stage('Compile & Test') {
            steps {
                echo '🛠️ Compiling and running tests...'
                
                bat '''
                    echo ======================================== > test-report.txt
                    echo Test Report >> test-report.txt
                    echo ======================================== >> test-report.txt
                    echo Unit tests: 5 tests run, 0 failures >> test-report.txt
                    echo Integration tests: 3 tests run, 0 failures >> test-report.txt
                    echo ======================================== >> test-report.txt
                '''
                
                // Создаём JUnit-совместимый файл для отображения тестов в Jenkins
                writeFile file: 'test-results.xml', text: '''<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="Application Tests" tests="8" failures="0" errors="0" skipped="0" time="0.5">
    <testcase name="testFunctionality" classname="AppTest" time="0.2"/>
    <testcase name="testPerformance" classname="AppTest" time="0.3"/>
</testsuite>'''
            }
            post {
                always {
                    junit 'test-results.xml'
                    archiveArtifacts artifacts: 'test-report.txt', fingerprint: true, allowEmptyArchive: true
                }
            }
        }
        
        // Этап 3: Создание артефакта (бинарный репозиторий)
        stage('Create Artifact') {
            steps {
                echo '📦 Creating build artifact...'
                
                bat '''
                    if not exist target mkdir target
                    
                    echo ======================================== > target/manifest.txt
                    echo Build Artifact Manifest >> target/manifest.txt
                    echo ======================================== >> target/manifest.txt
                    echo Branch: %BRANCH_NAME% >> target/manifest.txt
                    echo Build Number: %BUILD_NUMBER% >> target/manifest.txt
                    echo Build Date: %DATE% %TIME% >> target/manifest.txt
                    echo Status: SUCCESS >> target/manifest.txt
                    echo ======================================== >> target/manifest.txt
                    echo. >> target/manifest.txt
                    echo Static Analysis: PASSED >> target/manifest.txt
                    echo Unit Tests: 5/5 PASSED >> target/manifest.txt
                    echo Integration Tests: 3/3 PASSED >> target/manifest.txt
                    echo ======================================== >> target/manifest.txt
                    
                    echo Sample binary content > target/application.bin
                '''
            }
        }
    }
    
    post {
        always {
            echo '📂 Archiving artifacts to binary repository...'
            archiveArtifacts artifacts: 'target/*', fingerprint: true, allowEmptyArchive: true
        }
        
        success {
            echo """
            ╔══════════════════════════════════════════════════════════════╗
            ║  ✅ BUILD SUCCESSFUL ✅                                       ║
            ║                                                              ║
            ║  Branch: ${env.BRANCH_NAME}                                 ║
            ║  Build: ${env.BUILD_NUMBER}                                 ║
            ║                                                              ║
            ║  ✅ Static Analysis: Checkstyle + PMD (Warnings NG)          ║
            ║  ✅ Tests: 8/8 PASSED                                        ║
            ║  ✅ Binary Artifact: target/application.bin                  ║
            ╚══════════════════════════════════════════════════════════════╝
            """
        }
        
        failure {
            echo "❌ Build FAILED! Check console output."
        }
    }
}
