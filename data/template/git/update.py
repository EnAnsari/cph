import subprocess
import os

def run_command(command, cwd=os.path.dirname(os.path.abspath(__file__))):
    try:
        result = subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error while executing {command}:\n{e.stderr}")
        pass

def pull_changes():
    print("Pulling latest changes...")
    run_command(["git", "pull"])

def commit_changes():
    print("Committing changes...")
    run_command(["git", "add", "."])
    run_command(["git", "commit", "-m", 'Updated by update.py'])

def push_changes():
    print("Pushing changes...")
    run_command(["git", "push"])

if __name__ == "__main__":
    pull_changes()
    commit_changes()
    push_changes()
