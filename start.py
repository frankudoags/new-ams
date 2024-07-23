import subprocess


def start():
    subprocess.run(
        ["uvicorn", "app.main:app", "--reload"]
    )


if __name__ == "__main__":
    start()
