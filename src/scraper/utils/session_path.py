import os


session_files_path = os.path.abspath(os.path.join(os.path.realpath(__file__), '..', '..', "sessions"))


def get_session_path(username):
    session_path = os.path.join(session_files_path, username)
    return session_path
