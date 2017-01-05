def create_user_link(data):
    username = data.actor.username
    userprofile = data.actor.links.html.href
    avatar = data.actor.links.avatar.href

    return '![](%s) [%s](%s)' % (avatar, username, userprofile)


def create_repo_link(data):
    return '[%s](%s)' % (data.repository.full_name,
                         data.repository.links.html.href)
