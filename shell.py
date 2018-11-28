#!/usr/bin/env python3
import os

def handle_cd(command):
    # got to HOME
    if len(command) == 1 or command[1] == "~":
        if "HOME" in os.environ.keys():
            os.chdir(os.environ["HOME"])
        else:
            print("intek-sh: cd: HOME not set")
    elif command[1] == "-":
        os.chdir(os.environ["OLDPWD"])
    elif os.path.isfile(command[1]) is True:
        print("bash: cd: %s: Not a directory" % command[1])
    elif os.path.isdir(command[1]) is False:
        print("bash: cd: %s: No such file or directory" % command[1])
    else:
        os.chdir(command[1])
    return 1


def handle_printenv(command):
    list_show = command[1:]
    # show the vars these are confered
    if len(list_show) > 0:
        for var in list_show:
            if var in os.environ.keys():
                print(os.environ[var])
    # show all variables in env
    else:
        for key in os.environ:
            print(key + "=" + os.environ[key])


def handle_export(command):
    list_export = command[1:]
    for item in list_export:
        if "=" in item:
            key = item.split("=")[0]
            value = item.split("=")[1]
            os.environ.update({key: value})
        else:
            os.environ.update({item: ''})


def handle_unset(command):
    list_unset = command[1:]
    for key in list_unset:
        if key in os.environ.keys():
            del os.environ[key]


def handle_exit(command):
    print("exit")
    if len(command) != 1:
        try:
            int(command[1])
        except ValueError:
            print("intek-sh: exit:")
    return False


def handle_other_action(command):
    import subprocess
    import os
    try:
        if "./" in command[0]:
            subprocess.run(command)
            return
        path_list = handle_PATH()
        if path_list != []:
            for path in path_list:
                if os.path.exists(path + "/" + str(command[0])) is True:
                    if isRun(path + "/" + str(command[0])) is True:
                        subprocess.run(command)
                        return
        print("intek-sh: %s: command not found" % command[0])
    except PermissionError:
        print("intek-sh: %s: Permission denied" % str(command[0]))
        return
    except FileNotFoundError:
        print("intek-sh: " + command[0] + ": No such file or directory")
    except OSError:
        print("intek-sh: %s: command not found" % command[0])


def isRun(filepath):
    import os
    import stat
    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IRGRP)
    # Group: read and execute Permission


def handle_PATH():
    import os
    if 'PATH' not in os.environ:
        return []
    elif ':' in os.environ['PATH']:
        return os.environ['PATH'].split(':')
    elif '.' in os.environ['PATH']:
        return [os.getcwd()]


def handle_minish(command, run_minish):
    valid_command = ["cd", "printenv", "export", "unset", "exit"]
    if command[0] == valid_command[0]:
        handle_cd(command)
    elif command[0] == valid_command[1]:
        handle_printenv(command)
    elif command[0] == valid_command[2]:
        handle_export(command)
    elif command[0] == valid_command[3]:
        handle_unset(command)
    elif command[0] == valid_command[4]:
        run_minish = handle_exit(command)
    elif command[0] not in valid_command:
        handle_other_action(command)
    return run_minish


def main():
    run_minish = True
    while run_minish:
        try:
            commands = input("intek-sh$ ")
        except EOFError:
            return
        if commands != '':
            commands = commands.split("\\n")
            for com in commands:
                com = com.split()
                if handle_minish(com, run_minish) is False:
                    return


main()
