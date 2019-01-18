pipeline {
  agent any
  stages {
    stage('Setup') {
      steps {
        cleanWs()
        checkout([
          $class: 'GitSCM', branches: [ [ name: '*/master' ] ],
          doGenerateSubmoduleConfigurations: false, extensions: [ [
            $class: 'RelativeTargetDirectory', relativeTargetDir: 'mathematics'
          ] ],
          submoduleCfg: [],
          userRemoteConfigs:
              [ [ url: 'https://github.com/emilberwald/mathematics.git' ] ]
        ])
      }
    }
    stage('Analyze') {
      steps {
        sh label: 'Install dependencies', script: 'pip3 install pylint'
        dir('mathematics/src') {
          sh label: 'Pylint',
              script:
                  'python3 -m pylint --msg-template=\'{path}:{line}: [{msg_id}, {obj}] {msg} ({symbol})\' mathematics | tee ${WORKSPACE}/pylint.log'
        }
        recordIssues(tools: [ pyLint(pattern: 'pylint.log') ])
        archiveArtifacts artifacts: 'pylint.log', onlyIfSuccessful: true
      }
    }
    stage('Test') {
      steps {
        script {
          sh label: 'Install dependencies',
              script:
                  'pip3 install pytest pytest-timeout pytest-cov sympy parameterized numpy networkx scipy'
          try {
            timeout(time: 60, unit: 'SECONDS') {
              sh label: 'Test',
                  script:
                      'python3 -m pytest --cov-report xml:${WORKSPACE}/cov.xml --cov=mathematics --ignore="${WORKSPACE}/mathematics/src/mathematics/tools/presentation/test_graphical.py" --junitxml=${WORKSPACE}/junit.xml'
            }
          } catch (Exception e) {
            echo e.toString()
          }
        }
        cobertura autoUpdateHealth: false, autoUpdateStability: false,
            coberturaReportFile: 'cov.xml',
            conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false,
            failUnstable: false, lineCoverageTargets: '80, 0, 0',
            maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0',
            onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
      }
    }
    stage('Archive') {
      steps {
        junit allowEmptyResults: true, testResults: '*.xml'
        archiveArtifacts artifacts: '*.xml', onlyIfSuccessful: true
      }
    }
  }
}
