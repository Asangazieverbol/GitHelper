import subprocess
import sys

def run_git_command(args):
    try:
        output = subprocess.check_output(['git'] + args, stderr=subprocess.STDOUT)
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print(f" Ошибка: {e.output.decode()}")

def show_status():
    print(" Git Status:")
    run_git_command(["status"])

def create_branch(branch_type, name):
    branch_name = f"{branch_type}/{name}"
    print(f" Создание новой ветки: {branch_name}")
    run_git_command(["checkout", "-b", branch_name])
    run_git_command(["push", "-u", "origin", branch_name])

def commit_changes(message):
    print(" Добавление всех файлов и коммит...")
    run_git_command(["add", "."])
    run_git_command(["commit", "-m", message])
    run_git_command(["push"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
        Использование:
            python githelper.py status
            python githelper.py new-branch [тип] [название]
            python githelper.py commit [сообщение]
        """)
        sys.exit()

    command = sys.argv[1]

    if command == "status":
        show_status()
    elif command == "new-branch":
        if len(sys.argv) != 4:
            print("Пример: python githelper.py new-branch feature login-page")
        else:
            create_branch(sys.argv[2], sys.argv[3])
    elif command == "commit":
        if len(sys.argv) < 3:
            print("Укажите сообщение коммита")
        else:
            commit_message = " ".join(sys.argv[2:])
            commit_changes(commit_message)
    else:
        print(" Неизвестная команда")
