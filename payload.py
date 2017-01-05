

def _get_default_data():
    return {
                'color': '#FFFFFF',
                'text': 'Not implemented'
    }

def repo_push(data):
    resp = _get_default_data()
    resp['author_name'] = '%s (%s)' % (data.actor.display_name,
                                       data.actor.username)
    resp['author_icon'] = data.actor.links.avatar.href
    resp['author_link'] = data.actor.links.html.href

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
    resp['text'] = 'Pushed %s changesets to %s at %s\n%s' % (changesets,
                                                             branch,
                                                             repo_link,
                                                             '\n'.join(commits))
    return resp