#!/usr/bin/env groovy

node {
    update_commit_status('justbeay', 'jenkinsci-test', params.PULL_REQUEST_NUMBER, 'pending')
    echo "======== TRIGGER_BRANCH:${params.TRIGGER_BRANCH}, TRIGGER_Boolean:${params.TRIGGER_Boolean}, TRIGGER_Choice:${params.TRIGGER_Choice} ======="
    stage 'compile'
    dir('src'){
        checkout([
            $class: 'GitSCM',
            branches: [[name: params.TRIGGER_BRANCH]],
            doGenerateSubmoduleConfigurations: false,
            extensions: [[$class: 'CleanBeforeCheckout']],
            submoduleCfg: [],
            userRemoteConfigs: [[
                url: 'git@github.com:justbeay/jenkinsci-test.git'
            ]]
        ])
        sh "mvn clean install"
    }
    // stage 'deploy'
    echo "======== finish ${env.JOB_NAME}, with build number:${env.BUILD_NUMBER} ========"
    update_commit_status('justbeay', 'jenkinsci-test', params.PULL_REQUEST_NUMBER, 'success')
}

def update_commit_status(owner, repository, pullNumber, state) {
    if(pullNumber){
        withCredentials([usernamePassword(credentialsId: 'GITHUB_ACCESS_TOKEN', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]){
            sh "./src/script/git_commit_status.py --user ${USERNAME} --token ${PASSWORD}" +
                " --owner ${owner}" +
                " --repository ${repository}" +
                " --pull-number ${pullNumber}" +
                " --state ${state}" +
                // " --target-url '${BUILD_URL}'"
                " --description 'jenkins build job:${BUILD_NUMBER} ${state}'"
                " --context 'continuous-integration/jenkins'"
        }
    }
}