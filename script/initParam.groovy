#!/usr/bin/env groovy

properties([
    parameters([
        string(name: 'TRIGGER_BRANCH', defaultValue: 'dev', description: 'the git branch name', trim: false),
        booleanParam(name: 'TRIGGER_Boolean', defaultValue: true, description: 'service triigger'),
        choice(name: 'TRIGGER_Choice', choices: 'aaa\nbbb\nccc\nxxx\nyyy', defaultValue: 'xxx', description: ''),
        string(name: 'NOTICE_EMAIL', defaultValue: '', description: '	build result log email receiver, split by \';\'', trim: false),
        string(name: 'PULL_REQUEST_NUMBER', defaultValue: '', description: 'github pull_request number, used to update pull commits status', trim: false)
    ]),
    pipelineTriggers([
        parameterizedCron('H(0-5) 0 * * 1 % TRIGGER_Boolean=true')
    ])
])