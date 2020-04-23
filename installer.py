import os, subprocess

print("Starting script")

def is_tool(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno = os.errno.ENOENT:
            return False
    return True

is_tool(git)
is_tool(tmux)