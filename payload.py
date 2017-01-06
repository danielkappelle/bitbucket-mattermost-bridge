

def _get_default_data():
    return {
                'color': '#FFFFFF',
                'text': 'Not implemented'
    }


def _set_color_from_priority(priority):
    return {
        'trivial': '#205081',
        'minor': 'good',
        'major': 'warning',
        'critical': 'danger',
        'blocker': '#000000'
    }.get(priority, '#FFFFFF')

def _set_color_from_state(state):
    return {
        'SUCCESSFUL': 'good',
        'FAILED': 'danger'
    }.get(state, 'warning')


def _get_issue(data, action):
    resp = _get_default_data()
    resp = _set_author_infos(resp, data)
    template = '%s a %s %s [#%s: %s](%s) (%s)'

    issue = data.issue
    resp['text'] = template % (action, issue.priority, issue.type, issue.id,
                               issue.title, issue.links.html.href, issue.state)

    resp['color'] = _set_color_from_priority(issue.priority)
    return resp


def _get_pullrequest(data, action):
    resp = _get_default_data()
    resp = _set_author_infos(resp, data)

    pr = data.pullrequest
    pr_link = '[%s](%s)' % (pr.title, pr.links.html.href)
    pr_src_link = '%s/branch/%s' % (pr.source.repository.links.html.href,
                                    pr.source.branch.name)
    pr_dst_link = '%s/branch/%s' % (pr.destination.repository.links.html.href,
                                    pr.destination.branch.name)
    pr_src = '[%s:%s](%s)' % (pr.source.repository.full_name,
                              pr.source.branch.name,
                              pr_src_link)
    pr_dst = '[%s:%s](%s)' % (pr.destination.repository.full_name,
                              pr.destination.branch.name,
                              pr_dst_link)
    template = '%s pull request %s\nFrom %s to %s'
    resp['text'] = template % (action, pr_link, pr_src, pr_dst)

    return resp


def _set_author_infos(resp, data):
    if data.actor.display_name == 'Anonymous':
        resp['author_name'] = data.actor.display_name
        return resp

    resp['author_name'] = '%s (%s)' % (data.actor.display_name,
                                       data.actor.username)
    resp['author_icon'] = data.actor.links.avatar.href
    resp['author_link'] = data.actor.links.html.href

    return resp


def issue_comment_created(data):
    resp = _get_issue(data, 'Commented')
    return resp


def issue_created(data):
    resp = _get_issue(data, 'Opened')
    return resp


def issue_updated(data):
    resp = _get_issue(data, 'Updated')
    return resp


def repo_commit_comment_created(data):
    resp = _get_default_data()
    resp = _set_author_infos(resp, data)

    template = 'Commented commit %s at %s'
    commit_link = '[#%s](%s)' % (data.comment.commit.hash[:7],
                                 data.comment.links.html.href)
    repo_link = '[%s](%s)' % (data.repository.full_name,
                              data.repository.links.html.href)
    resp['text'] = template % (commit_link, repo_link)

    return resp


def repo_commit_status_created(data):
    resp = _get_default_data()
    resp = _set_author_infos(resp, data)

    ci_link = '[%s](%s)' % (data.commit_status.key, data.commit_status.url)
    resp['text'] = 'Launch CI build on %s' % ci_link

    return resp


def repo_commit_status_updated(data):
    resp = _get_default_data()
    resp = _set_author_infos(resp, data)

    ci_link = '[%s](%s)' % (data.commit_status.key, data.commit_status.url)
    resp['text'] = 'CI build on %s is finished' % ci_link
    resp['color'] = _set_color_from_state(data.commit_status.state)

    return resp


def repo_fork(data):
    resp = _get_default_data()
    resp = _set_author_infos(resp, data)

    template = 'Forked %s to %s'
    src_link = '[%s](%s)' % (data.repository.full_name,
                             data.repository.links.html.href)
    dst_link = '[%s](%s)' % (data.fork.full_name, data.fork.links.html.href)
    resp['text'] = template % (src_link, dst_link)

    return resp


def repo_push(data):
    resp = _get_default_data()
    resp = _set_author_infos(resp, data)

    changesets = len(data.push.changes[0].commits)
    repo_link = '[%s](%s)' % (data.repository.full_name,
                              data.repository.links.html.href)
    branch = data.push.changes[0].new.name
    commits = []
    for commit in data.push.changes[0].commits:
        text = '- [%s](%s): %s' % (commit.hash[:7],
                                   commit.links.html.href,
                                   commit.message.strip().replace('\n', ' - '))
        commits.append(text)
    template = 'Pushed %s changesets to %s at %s\n%s'
    resp['text'] = template % (changesets, branch,
                               repo_link, '\n'.join(commits))
    return resp


def repo_updated(data):
    resp = _get_default_data()
    resp = _set_author_infos(resp, data)
    repo_link = '[%s](%s)' % (data.repository.full_name,
                              data.repository.links.html.href)

    resp['text'] = 'Updated repo %s' % repo_link
    return resp


def pullrequest_approved(data):
    resp = _get_pullrequest(data, 'Approved')
    return resp


def pullrequest_created(data):
    resp = _get_pullrequest(data, 'Opened')
    return resp


def pullrequest_fulfilled(data):
    resp = _get_pullrequest(data, 'Merged')
    return resp


def pullrequest_rejected(data):
    resp = _get_pullrequest(data, 'Rejected')
    return resp


def pullrequest_updated(data):
    resp = _get_pullrequest(data, 'Updated')
    return resp


def pullrequest_unapproved(data):
    resp = _get_pullrequest(data, 'Unapproved')
    return resp


def pullrequest_comment_created(data):
    resp = _get_pullrequest(data, 'Left a comment on the')
    return resp


def pullrequest_comment_updated(data):
    resp = _get_pullrequest(data, 'Updated a comment he left on the')
    return resp


def pullrequest_comment_deleted(data):
    resp = _get_pullrequest(data, 'Deleted a comment he left on the')
    return resp
