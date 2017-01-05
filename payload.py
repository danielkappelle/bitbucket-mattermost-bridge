

def _get_default_data():
    return {
        'attachments': [
            {
                'color': '#FFFFFF',
                'text': 'Not implemented'
            }
        ]
    }

def repo_push(data):
    resp = _get_default_data()
    resp['author_name'] = data.actor.username
    resp['author_icon'] = data.actor.links.avatar.href
    resp['author_link'] = data.actor.links.html.href

    changesets = len(data.push.changes[0].commits)
    repo_link = '[%s](%s)' % (data.repository.full_name,
                              data.repository.links.html.href)
    branch = data.push.changes[0].new.name
    resp['text'] = 'Pushed %s changesets to %s at %s' % (changesets,
                                                         branch,
                                                         repo_link)
    return resp