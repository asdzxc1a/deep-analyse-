import os
from pathlib import Path


class ExampleRunner:
    def __init__(self, root: Path) -> None:
        self.root = root

    def run(self) -> str:
        return os.getenv("APP_MODE", "dev")


def load_config(config_path: Path) -> dict[str, str]:
    return {"path": str(config_path)}


def main() -> None:
    runner = ExampleRunner(Path.cwd())
    print(runner.run())


if __name__ == "__main__":
    main()
