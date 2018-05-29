#!/usr/bin/env groovy

properties([
    parameters([
        string(name: 'TRIGGER_BRANCH', defaultValue: 'dev', description: 'the git branch name', trim: false),
        booleanParam(name: 'TRIGGER_Boolean', defaultValue: true, description: 'service triigger'),
        choice(name: 'TRIGGER_Choice', choices: 'aaa\nbbb\nccc\nxxx\nyyy', defaultValue: 'xxx', description: '')
    ]),
    pipelineTriggers([
        parameterizedCron('H/3 * * * * % TRIGGER_Boolean=true')
    ])
])