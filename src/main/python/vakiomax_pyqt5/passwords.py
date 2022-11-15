import subprocess

app_name = 'vakiomax4-pyqt5'


def set_password(username, password):
    return subprocess.run(['security', 'add-generic-password', '-U', '-a', username, '-s', app_name, '-w', password])


def get_password(username):
    return subprocess.run(['security', 'find-generic-password', '-w', '-s', app_name, '-a', username],
                          capture_output=True).stdout.decode('utf-8').strip()
