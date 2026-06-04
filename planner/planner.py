import subprocess


def run_planner(domain_file, problem_file):

    command = [
        "wsl",
        "python3",
        "/home/ghadeer_rady/downward/fast-downward.py",
        "--alias",
        "seq-sat-lama-2011",
        domain_file,
        problem_file
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    print("STDOUT:")
    print(result.stdout)

    print("\nSTDERR:")
    print(result.stderr)

    print("\nRETURN CODE:")
    print(result.returncode)

    return result.stdout