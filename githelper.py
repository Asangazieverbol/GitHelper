import subprocess
import sys
import os

def run_command(cmd, is_svn=False):
    prefix = ['svn'] if is_svn else ['git']
    try:
        result = subprocess.check_output(prefix + cmd, stderr=subprocess.STDOUT)
        print(result.decode())
    except subprocess.CalledProcessError as e:
        print("Ошибка:", e.output.decode())

def show_status(is_svn=False):
    print(" Статус:")
    run_command(['status'], is_svn)

def create_branch(branch_type, name, is_svn=False):
    branch_name = f"{branch_type}/{name}"
    print(f"Создание ветки: {branch_name}")
    if is_svn:
        trunk_url = "https://localhost/svn/TestRepo/trunk"
        branches_url = f"https://localhost/svn/TestRepo/branches/{branch_name}"
        run_command(["copy", trunk_url, branches_url, "-m", f"Создана ветка {branch_name}"], True)
    else:
        run_command(['checkout', '-b', branch_name])
        run_command(['push', '-u', 'origin', branch_name])

def commit_changes(message, is_svn=False):
    print("Добавление и коммит...")
    if is_svn:
        run_command(["add", "--force", "."], True)
        run_command(["commit", "-m", message], True)
    else:
        run_command(["add", "."])
        run_command(["commit", "-m", message])
        run_command(["push"])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("""
        Использование:
            python githelper.py git status
            python githelper.py git new-branch [тип] [название]
            python githelper.py git commit [сообщение]
            python githelper.py svn status
            python githelper.py svn commit [сообщение]
        """)
        sys.exit()

    mode = sys.argv[1]  # git или svn
    command = sys.argv[2]
    is_svn = (mode == 'svn')

    if command == "status":
        show_status(is_svn)
    elif command == "new-branch":
        if len(sys.argv) != 5:
            print("Пример: python githelper.py git new-branch feature login-page")
        else:
            create_branch(sys.argv[3], sys.argv[4], is_svn)
    elif command == "commit":
        if len(sys.argv) < 4:
            print("Укажите сообщение коммита")
        else:
            commit_message = " ".join(sys.argv[3:])
            commit_changes(commit_message, is_svn)
    else:
        print("Неизвестная команда")
