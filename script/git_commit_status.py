#!/usr/bin/env python3

import sys
import argparse
from urllib import request
import ssl
import json

def parse_input(paramStr):
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', help='github user to login', required=True)
    parser.add_argument('--token', help='github user token to login', required=True)
    parser.add_argument('--owner', help='github repository owner', required=True)
    parser.add_argument('--repository', help='github repository name', required=True)
    parser.add_argument('--pull-number', help='pull request number', required=False, type=int)
    parser.add_argument('--commit-ids', help='list of paths to clear, default /*', nargs='+', required=False)
    parser.add_argument('--state', help='the state of the status. Can be one of error, failure, pending, or success', required=True)
    parser.add_argument('--target-url', help='target URL to associate with this status', required=False)
    parser.add_argument('--description', help='a short description of the status', required=False)
    parser.add_argument('--context', help='a string label to differentiate this status from the status of other systems', required=False)
    args = parser.parse_args(paramStr)
    if not args.pull_number and not args.commit_ids:
        print('--pull-number and --commit-ids cannot be empty both', file=sys.stderr)
        sys.exit(1)
    return args

def get_auth_opener(host, user, token):
    passman = request.HTTPPasswordMgrWithPriorAuth()
    passman.add_password(None, host, user, token, is_authenticated=True)
    auth_handler = request.HTTPBasicAuthHandler(passman)
    ssl._create_default_https_context = ssl._create_unverified_context
    opener = request.build_opener(auth_handler)
    # opener.add_handler(request.ProxyHandler(dict(http='http://127.0.0.1:5555')))
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    request.install_opener(opener)
    return opener

def update_commit_status(owner, repository, commit_id, state, target_url='', description='', context='default', opener=None):
    global api_host
    print('update repository(%s/%s)\'s commit: %s status to state: %s' % (owner, repository, commit_id, state))
    opener = get_auth_opener(api_host, args.user, args.token) if not opener else opener
    api_url = '%s/repos/%s/%s/statuses/%s' % (api_host, owner, repository, commit_id)
    json_post = dict(state=state, target_url=target_url, description=description, context=context)
    req = request.Request(url = api_url,
                                data = json.dumps(json_post).encode(encoding='utf-8'),
                                headers = {'Content-Type': 'application/json'},
                                method = 'POST')
    print(api_url)
    opener.open(req)

def get_pull_detail(owner, repository, pull_number, opener=None):
    global api_host
    opener = get_auth_opener(api_host, args.user, args.token) if not opener else opener
    api_url = '%s/repos/%s/%s/pulls/%d' % (api_host, owner, repository, pull_number)
    req = request.Request(url = api_url, method = 'GET')
    res = opener.open(req)
    json_result = json.loads(res.read().decode('utf-8'))
    res.close()
    return json_result

def get_pull_commits(owner, repository, pull_number, opener=None):
    global api_host
    opener = get_auth_opener(api_host, args.user, args.token) if not opener else opener
    api_url = '%s/repos/%s/%s/pulls/%d/commits' % (api_host, owner, repository, pull_number)
    req = request.Request(url = api_url, method = 'GET')
    res = opener.open(req)
    json_result = json.loads(res.read().decode('utf-8'))
    res.close()
    return json_result


args = parse_input(sys.argv[1:])
api_host = 'https://api.github.com'
auth_opener = get_auth_opener(api_host, args.user, args.token)
commit_ids = args.commit_ids if args.commit_ids else []
commit_author = args.owner
commit_repository = args.repository
if args.pull_number:
    # get pull detail
    pull_detail = get_pull_detail(args.owner, args.repository, args.pull_number, opener=auth_opener)
    commit_author = pull_detail['head']['user']['login']
    commit_repository = pull_detail['head']['repo']['name']
    # get pull's all commit
    commits = get_pull_commits(args.owner, args.repository, args.pull_number, opener=auth_opener)
    for commit in commits:
        commit_ids.append(commit['sha'])
# update commit status
for commit_id in commit_ids:
    update_commit_status(args.owner, args.repository, commit_id, 
            state=args.state, target_url=args.target_url, description=args.description,
            context='continuous-integration/jenkins')
