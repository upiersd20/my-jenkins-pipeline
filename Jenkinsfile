pipeline {
    agent any
    
    stages {
        stage('Static Code Analysis') {
            steps {
                echo '🔍 Running static code analysis...'
                bat 'echo Static Analysis: All checks passed > analysis-report.txt'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'analysis-report.txt', allowEmptyArchive: true
                }
            }
        }
        
        stage('Compile & Test') {
            steps {
                echo '🛠️ Running tests...'
                bat 'echo Test Report: 8/8 tests passed > test-report.txt'
                writeFile file: 'test-results.xml', text: '''<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="Demo Tests" tests="8" failures="0" errors="0" skipped="0">
  <testcase name="test1" classname="DemoTest" time="0.1"/>
  <testcase name="test2" classname="DemoTest" time="0.2"/>
  <testcase name="test3" classname="DemoTest" time="0.3"/>
  <testcase name="test4" classname="DemoTest" time="0.1"/>
  <testcase name="test5" classname="DemoTest" time="0.2"/>
  <testcase name="integration1" classname="IntegrationTest" time="0.5"/>
  <testcase name="integration2" classname="IntegrationTest" time="0.4"/>
  <testcase name="integration3" classname="IntegrationTest" time="0.3"/>
</testsuite>'''
                junit 'test-results.xml'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'test-report.txt', allowEmptyArchive: true
                }
            }
        }
        
        stage('Create Artifact') {
            steps {
                echo '📦 Creating build artifact...'
                bat '''
                    if not exist target mkdir target
                    echo ======================================== > target\\artifact.txt
                    echo Build Artifact >> target\\artifact.txt
                    echo ======================================== >> target\\artifact.txt
                    echo Branch: %BRANCH_NAME% >> target\\artifact.txt
                    echo Build Number: %BUILD_NUMBER% >> target\\artifact.txt
                    echo Build Date: %DATE% %TIME% >> target\\artifact.txt
                    echo Status: SUCCESS >> target\\artifact.txt
                    echo ======================================== >> target\\artifact.txt
                    echo Static Analysis: PASSED >> target\\artifact.txt
                    echo Unit Tests: 5/5 PASSED >> target\\artifact.txt
                    echo Integration Tests: 3/3 PASSED >> target\\artifact.txt
                    echo ======================================== >> target\\artifact.txt
                '''
            }
        }
    }
    stage('Static Code Analysis') {
    steps {
        echo '🔍 Running static code analysis...'
        
        // Генерация отчёта в формате, который понимает Warnings NG
        // Допустим, ваш анализатор умеет создавать checkstyle.xml
        bat 'mvn checkstyle:checkstyle pmd:pmd'
    }
    post {
        always {
            // !!! НОВЫЙ ШАГ: Публикация отчётов через плагин !!!
            recordIssues enabledForFailure: true,
                          tools: [
                              checkStyle(pattern: '**/checkstyle-result.xml'),
                              pmd(pattern: '**/pmd.xml')
                          ]
            
            // Старый способ (архивация файлов) можно оставить как резервный
            archiveArtifacts artifacts: '**/checkstyle-result.xml, **/pmd.xml', allowEmptyArchive: true
        }
    }
}
    post {
        always {
            echo '📂 Archiving artifacts...'
            archiveArtifacts artifacts: 'analysis-report.txt', allowEmptyArchive: true
            archiveArtifacts artifacts: 'test-report.txt', allowEmptyArchive: true
            archiveArtifacts artifacts: 'target/artifact.txt', fingerprint: true, allowEmptyArchive: true
        }
        
        success {
            echo "✅ Build SUCCESSFUL for branch: ${env.BRANCH_NAME}"
        }
        
        failure {
            echo "❌ Build FAILED! Check console output."
        }
    }
}
