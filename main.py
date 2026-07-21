from cli import run_cli
from command.command_handler import CommandHandler
from core.mini_redis import MiniRedis


def main() -> None:
    redis = MiniRedis()
    handler = CommandHandler(redis)

    run_cli(handler)


if __name__ == "__main__":
    main()