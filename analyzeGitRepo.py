import os
import subprocess
import csv
import tempfile
import shutil
from typing import Dict


def clone_repo(repo_url: str, clone_dir: str) -> None:
    subprocess.run(['git', 'clone', repo_url, clone_dir], check=True)


def get_file_changes(repo_path: str) -> Dict[str, int]:
    os.chdir(repo_path)

    result = subprocess.run(
        ['git', 'log', '--name-only', '--pretty=format:'],
        stdout=subprocess.PIPE, text=True, check=True
    )

    file_changes = {}

    for line in result.stdout.splitlines():
        if line.strip():  # Ignore Empty
            if line not in file_changes:
                file_changes[line] = 0
            file_changes[line] += 1

    return file_changes


def save_to_csv(file_changes: Dict[str, int], output_file: str) -> None:
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File', 'Number of Changes'])

        for file_name, change_count in file_changes.items():
            writer.writerow([file_name, change_count])


def analyze_repo(repo_url: str, output_csv: str) -> None:
    # Create a permanent directory instead of using TemporaryDirectory
    temp_dir = tempfile.mkdtemp()

    try:
        clone_repo(repo_url, temp_dir)
        file_changes = get_file_changes(temp_dir)
        save_to_csv(file_changes, output_csv)
    finally:
        # Remove the directory explicitly only after everything is done
        try:
            shutil.rmtree(temp_dir)
        except PermissionError:
            print(f"Warning: Could not remove the temp directory {temp_dir}. It might still be in use.")


if __name__ == "__main__":
    repo_options = {
        '1': "https://github.com/apache/openoffice.git",
        '2': "https://github.com/apache/lucene.git",
        '3': "https://github.com/apache/maven.git",
        '4': "https://github.com/vprusso/toqito.git",
        '5': "https://github.com/OpenBB-finance/OpenBB.git",
        '6': "https://github.com/ShareX/ShareX.git",
        '7': "https://github.com/d2phap/ImageGlass.git"
    }

    print("Choose a repo to analyze:")
    print("1. Open Office")
    print("2. Lucene")
    print("3. Maven")
    print("4. Toqito")
    print("5. OpenBB")
    print("6. ShareX")
    print("7. ImageGlass")
    print("8. Enter a custom repo URL\n")

    choice = input("Enter your choice (1/2/3/4/5/6/7/8): ").strip()

    if choice in repo_options:
        repo_url = repo_options[choice]
    elif choice == '8':
        repo_url = input("Enter the GitHub repo URL: ")
    else:
        print("Invalid choice. Exiting.")
        exit(1)

    repo_name = repo_url.rstrip('/').split('/')[-1]
    output_csv = f"{repo_name}_file_changes.csv"
    analyze_repo(repo_url, output_csv)
    print(f"Analysis complete! Results saved to {output_csv}")
