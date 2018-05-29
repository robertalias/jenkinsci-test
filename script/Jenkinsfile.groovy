#!/usr/bin/env groovy

node {
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
}