void addUsedDependencies() {
  sh label: 'Add used dependencies', script: '\
#!/bin/bash -x                                                          \n\
source "${WORKSPACE}/venv/bin/activate";                                \n\
python3 -m pip -V | tee -a "${WORKSPACE}/requirements.txt";             \n\
python3 -m pip freeze | tee -a "${WORKSPACE}/requirements.txt"'
}
pipeline {
  agent any
  stages {
    stage('Setup') {
      steps {
        sh label: "Uninstall python modules...", script: '\
#!/bin/bash -x                                                          \n\
pip3 uninstall -y -r <(pip3 freeze);                                    \n\
python3 -m pip uninstall -y -r <(python3 -m pip freeze);'
        sh label: 'Create python virtual environment', script: '\
#!/bin/bash -x                                                          \n\
python3 -m venv --clear --without-pip "${WORKSPACE}/venv";              \n\
source "${WORKSPACE}/venv/bin/activate";                                \n\
python3 -m ensurepip --upgrade;                                         \n\
python3 -m pip install -U pip;                                          \n\
if [ ! -f "${WORKSPACE}/requirements.txt" ];                            \n\
then                                                                    \n\
(python3 -m pip -V > "${WORKSPACE}/requirements.txt";                   \n\
python3 -m pip freeze | tee -a "${WORKSPACE}/requirements.txt");        \n\
fi'
      }
    }
    stage('Test') {
      steps {
        script {
          sh label: 'Install dependencies', script: '\
#!/bin/bash -x                                                          \n\
source "${WORKSPACE}/venv/bin/activate";                                \n\
python3 -m pip install -r ${WORKSPACE}/mathematics/requirements.txt'
          addUsedDependencies();
          try {
            timeout(time: 60, unit: 'SECONDS') {
              sh label: 'Test', script: '\
#!/bin/bash -x                                                                                                                                                                                          \n\
source "${WORKSPACE}/venv/bin/activate";                                                                                                                                                                \n\
python3 -m pytest --cov-report xml:${WORKSPACE}/cov.xml --cov=mathematics --ignore="${WORKSPACE}/mathematics/src/mathematics/tools/presentation/test_graphical.py" --junitxml=${WORKSPACE}/junit.xml'
            }
          } catch (Exception e) {
            echo e.toString()
          }
          addUsedDependencies();
        }
        cobertura autoUpdateHealth: false, autoUpdateStability: false,
            coberturaReportFile: 'cov.xml',
            conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false,
            failUnstable: false, lineCoverageTargets: '80, 0, 0',
            maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0',
            onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
      }
    }
    stage('Analyze') {
      steps {
        sh label: 'Install dependencies', script: '\
#!/bin/bash -x                              \n\
source "${WORKSPACE}/venv/bin/activate";    \n\
python3 -m pip install pylint'
        dir('mathematics/src') {
          sh label: 'Pylint', script: '\
#!/bin/bash -x                                                                                                                      \n\
source "${WORKSPACE}/venv/bin/activate";                                                                                            \n\
python3 -m pylint --msg-template=\'{abspath}:{line}: [{msg_id}, {obj}] {msg} ({symbol})\' mathematics | tee ${WORKSPACE}/pylint.log'
        }
        recordIssues(tools: [ pyLint(pattern: 'pylint.log') ])
        addUsedDependencies();
      }
    }
    stage('Archive') {
      steps {
        junit allowEmptyResults: true, testResults: '*.xml'
        archiveArtifacts artifacts: 'pylint.log', onlyIfSuccessful: false
        archiveArtifacts artifacts: '*.xml', onlyIfSuccessful: false
        archiveArtifacts artifacts: 'requirements.txt', onlyIfSuccessful: false
      }
    }
  }
}
