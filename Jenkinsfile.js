String inBash() { return '#!/bin/bash -x\n'; }
String inPythonVenv() { return 'source "${WORKSPACE}/venv/bin/activate";'; }
void addUsedDependencies(boolean init = false) {
    if (init) {
        sh label: 'Add used dependencies', script: [
            inBash(), inPythonVenv(),
            'python3 -m pip -V | tee "${WORKSPACE}/used_requirements.txt";',
            'python3 -m pip freeze | tee -a "${WORKSPACE}/used_requirements.txt";'
        ].join('\n')
    } else {
        sh label: 'Add used dependencies', script: [
            inBash(), inPythonVenv(),
            'python3 -m pip -V | tee -a "${WORKSPACE}/used_requirements.txt";',
            'python3 -m pip freeze | tee -a "${WORKSPACE}/used_requirements.txt";'
        ].join('\n')
    }
}
pipeline {
    agent any
    stages {
        stage('Setup') {
            steps{
                sh label: "Create python virtual environment...", script: [
                    inBash(), 'python3 -m venv --clear --without-pip "${WORKSPACE}/venv";'
                ].join('\n')
                sh label: "Install pip in virtual environment...", script: [
                    inBash(), inPythonVenv(), 'python3 -m ensurepip --upgrade;',
                    'python3 -m pip install -U pip;'
                ].join('\n')
            }
            post{
                always { addUsedDependencies(true) }
            }
        }
        stage('Test-Setup') {
            steps {
                sh label: 'Install dependencies', script: [
                    inBash(), inPythonVenv(),
                    'python3 -m pip install -r ${WORKSPACE}/requirements.txt'
                ].join('\n');
            }
        }
        stage('Test') {
            steps {
                script {
                    try {
                        timeout(time: 60, unit: 'SECONDS') {
                            sh label: 'Test', script: [
                                inBash(), inPythonVenv(),
                                'python3 -m pytest --cov-report xml:${WORKSPACE}/cov.xml --cov=mathematics --ignore="${WORKSPACE}/src/mathematics/tools/presentation/test_graphical.py" --junitxml=${WORKSPACE}/junit.xml'
                            ].join('\n');
                        }
                    } catch (Exception e) {
                        echo e.toString()
                    }
                }
            }
            post {
                always {
                    addUsedDependencies();
                    cobertura autoUpdateHealth: false, autoUpdateStability: false,
                        coberturaReportFile: 'cov.xml',
                            conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false,
                                failUnstable: false, lineCoverageTargets: '80, 0, 0',
                                    maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0',
                                        onlyStable: false, sourceEncoding: 'ASCII',
                                            zoomCoverageChart: false
                    junit allowEmptyResults: true, testResults: '*.xml'
                }
            }
        }
        stage('Analyze-Setup') {
            steps {
                sh label: 'Install dependencies', script: [
                    inBash(), inPythonVenv(), 'python3 -m pip install pylint'
                ].join('\n');
            }
        }
        stage('Analyze') {
            steps {
                dir('src') {
                    sh label: 'Pylint', script: [
                        inBash(), inPythonVenv(),
                        'python3 -m pylint --msg-template=\'{abspath}:{line}: [{msg_id}, {obj}] {msg} ({symbol})\' mathematics | tee ${WORKSPACE}/pylint.log'
                    ].join('\n')
                }
            }
            post {
                always {
                    addUsedDependencies();
                    recordIssues(tools: [pyLint(pattern: 'pylint.log')])
                    archiveArtifacts artifacts: 'pylint.log', onlyIfSuccessful: false
                }
            }
        }
        stage('Documentation') {
            environment{
                AUTHOR = "Emil Berwald"
                VERSION = "0.0.0"
                SPHINX_APIDOC_OPTIONS = "members,undoc-members,private-members,special-members,show-inheritance"
            }
            steps {
                sh label: 'Install sphinx', script: [
                    inBash(), inPythonVenv(), 'python3 -m pip install -U sphinx'
                ].join('\n');
                sh label: 'Run sphinx api-docs', script: [
                    inBash(),
                    inPythonVenv(),
                    'sphinx-apidoc --full -a -H ${JOB_NAME} -A "${AUTHOR}" -V "${VERSION}" -R "${VERSION}.${BUILD_NUMBER}" -o "${WORKSPACE}/docs" "${WORKSPACE}/src/";'
                ].join('\n');
                sh label: "Add mathjax to conf.py", script: [
                    inBash(),
                    ['echo', "'\nextensions.append(\"sphinx.ext.mathjax\")'", '>>"${WORKSPACE}/docs/conf.py";'].join(' '),
                    ['echo', "'\nmathjax_path=\"MathJax/MathJax.js?config=TeX-MML-AM_CHTML\"'", '>>"${WORKSPACE}/docs/conf.py";'].join(' '),
                    'mkdir -p \"${WORKSPACE}/docs/_static\";'
                ].join('\n')
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: 'docs/_static/MathJax'], [$class: 'CloneOption', noTags: true, reference: '', shallow: true]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/mathjax/MathJax.git']]])
                dir('docs') {
                    sh label: 'Run sphinx', script: [
                        inBash(),
                        inPythonVenv(),
                        'make html;'].join('\n');
                }
            }
            post{
                always{
                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: true, reportDir: 'docs/_build/html/', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                    archiveArtifacts artifacts: 'docs/*.*', onlyIfSuccessful: false
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'used_requirements.txt', onlyIfSuccessful: false
        }
    }
}