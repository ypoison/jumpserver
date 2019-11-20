    tasks = []
    if system_user.password:
        tasks.append({
            'name': 'Add user {}'.format(system_user.username),
            'action': {
                'module': 'user',
                'args': 'name={} shell={} state=present password={}'.format(
                    system_user.username, system_user.shell,
                    encrypt_password(system_user.password, salt="K3mIlKK"),
                ),
            }
        })