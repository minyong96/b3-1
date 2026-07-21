import shlex

from command.command_handler import CommandHandler


def run_cli(handler: CommandHandler) -> None:
    """
    Mini Redis REPL을 실행한다.

    큰따옴표로 감싼 공백 포함 문자열을 처리하기 위해
    shlex.split()을 사용한다.

    예:
        SET user:1 "Alice Kim"

    파싱 결과:
        ["SET", "user:1", "Alice Kim"]
    """
    while True:
        try:
            raw_command = input("mini-redis> ").strip()
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            break

        if raw_command == "":
            continue

        if raw_command.lower() in ("exit", "quit"):
            break

        try:
            args = shlex.split(raw_command)
        except ValueError:
            print("(error) ERR invalid syntax")
            continue

        result = handler.execute(args)
        print(result)