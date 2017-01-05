

def _get_default_data():
    return {
                'color': '#FFFFFF',
                'text': 'Not implemented'
    }

def _get_color_from_priority(priority):
    return {
        'trivial': '#205081',
        'minor': 'good',
        'major': 'warning',
        'critical': 'danger',
        'blocker': '#000000'
    }.get(priority, '#FFFFFF')

def set_author_infos(resp, data):
    if data.actor.display_name == 'Anonymous':
        resp['author_name'] = data.actor.display_name
        return resp

    resp['author_name'] = '%s (%s)' % (data.actor.display_name,
                                       data.actor.username)
    resp['author_icon'] = data.actor.links.avatar.href
    resp['author_link'] = data.actor.links.html.href

    return resp

def issue_created(data):
    resp = _get_default_data()
    resp = set_author_infos(resp, data)

    issue = data.issue
    template = 'Opened a %s %s [#%s: %s](%s) (%s)'
    resp['text'] = template % (issue.priority, issue.type, issue.id,
                               issue.title, issue.links.html.href, issue.state)

    resp['color'] = _get_color_from_priority(issue.priority)
    return resp

def issue_updated(data):
    resp = _get_default_data()
    resp = set_author_infos(resp, data)

    issue = data.issue
    template = 'Updated a %s %s [#%s: %s](%s) (%s)'
    resp['text'] = template % (issue.priority, issue.type, issue.id,
                               issue.title, issue.links.html.href, issue.state)

    resp['color'] = _get_color_from_priority(issue.priority)
    return resp

def repo_push(data):
    resp = _get_default_data()
    resp = set_author_infos(resp, data)

    changesets = len(data.push.changes[0].commits)
    repo_link = '[%s](%s)' % (data.repository.full_name,
                              data.repository.links.html.href)
    branch = data.push.changes[0].new.name
    commits = []
    for commit in data.push.changes[0].commits:
        text = '- [%s](%s): %s' % (commit.hash[:7],
                                 commit.links.html.href,
                                 commit.message)
        commits.append(text)
    resp['text'] = 'Pushed %s changesets to %s at %s\n> %s' % (changesets,
                                                             branch,
                                                             repo_link,
                                                             '\n'.join(commits))
    return resp