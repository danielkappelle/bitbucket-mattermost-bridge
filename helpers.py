def create_user_link(data):
    username = data.actor.username
    userprofile = data.actor.links.html.href
    avatar = data.actor.links.avatar.href

    return '![](%s) [%s](%s)' % (avatar, username, userprofile)
