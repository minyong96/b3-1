from core.mini_redis import MiniRedis


class CommandHandler:
    """
    파싱된 명령어를 검증하고 MiniRedis에 전달한다.

    MiniRedis:
        실제 데이터 및 정책 처리

    CommandHandler:
        명령어 검증 및 Redis 스타일 출력 변환
    """

    def __init__(self, redis: MiniRedis) -> None:
        self.redis = redis

    def execute(self, args: list[str]) -> str:
        """
        파싱된 명령어를 실행한다.

        예:
            ["SET", "user:1", "Alice"]
            ["GET", "user:1"]
            ["CONFIG", "SET", "maxmemory", "100"]
        """
        if len(args) == 0:
            return "(error) ERR empty command"

        command = args[0].upper()

        if command == "SET":
            return self._set(args)

        if command == "GET":
            return self._get(args)

        if command == "DEL":
            return self._delete(args)

        if command == "EXISTS":
            return self._exists(args)

        if command == "DBSIZE":
            return self._dbsize(args)

        if command == "KEYS":
            return self._keys(args)

        if command == "EXPIRE":
            return self._expire(args)

        if command == "TTL":
            return self._ttl(args)

        if command == "CONFIG":
            return self._config(args)

        if command == "INFO":
            return self._info(args)

        return (
            f"(error) ERR unknown command "
            f"'{args[0].lower()}'"
        )

    def _set(self, args: list[str]) -> str:
        if len(args) != 3:
            return self._wrong_arguments("SET")

        key = args[1]
        value = args[2]

        try:
            self.redis.set(key, value)
        except MemoryError:
            return (
                "(error) OOM command not allowed "
                "when used_memory > 'maxmemory'"
            )

        return "OK"

    def _get(self, args: list[str]) -> str:
        if len(args) != 2:
            return self._wrong_arguments("GET")

        key = args[1]
        value = self.redis.get(key)

        if value is None:
            return "(nil)"

        return f'"{value}"'

    def _delete(self, args: list[str]) -> str:
        if len(args) != 2:
            return self._wrong_arguments("DEL")

        deleted = self.redis.delete(args[1])

        if deleted:
            return "(integer) 1"

        return "(integer) 0"

    def _exists(self, args: list[str]) -> str:
        if len(args) != 2:
            return self._wrong_arguments("EXISTS")

        exists = self.redis.exists(args[1])

        if exists:
            return "(integer) 1"

        return "(integer) 0"

    def _dbsize(self, args: list[str]) -> str:
        if len(args) != 1:
            return self._wrong_arguments("DBSIZE")

        return f"(integer) {self.redis.dbsize()}"

    def _keys(self, args: list[str]) -> str:
        if len(args) != 1:
            return self._wrong_arguments("KEYS")

        keys = self.redis.keys()

        if len(keys) == 0:
            return "(empty array)"

        result = []

        for index, key in enumerate(keys, start=1):
            result.append(f'{index}. "{key}"')

        return "\n".join(result)

    def _expire(self, args: list[str]) -> str:
        if len(args) != 3:
            return self._wrong_arguments("EXPIRE")

        key = args[1]

        try:
            seconds = int(args[2])
        except ValueError:
            return self._invalid_integer()

        success = self.redis.expire(key, seconds)

        if success:
            return "(integer) 1"

        return "(integer) 0"

    def _ttl(self, args: list[str]) -> str:
        if len(args) != 2:
            return self._wrong_arguments("TTL")

        remaining = self.redis.ttl(args[1])

        return f"(integer) {remaining}"

    def _config(self, args: list[str]) -> str:
        """
        지원 형식:

        CONFIG SET maxmemory bytes
        """
        if len(args) != 4:
            return self._wrong_arguments("CONFIG")

        subcommand = args[1].upper()
        option = args[2].lower()

        if subcommand != "SET":
            return (
                "(error) ERR unsupported CONFIG subcommand "
                f"'{args[1]}'"
            )

        if option != "maxmemory":
            return (
                "(error) ERR unsupported CONFIG parameter "
                f"'{args[2]}'"
            )

        try:
            maxmemory = int(args[3])
        except ValueError:
            return self._invalid_integer()

        if maxmemory < 0:
            return self._invalid_integer()

        self.redis.set_maxmemory(maxmemory)

        return "OK"

    def _info(self, args: list[str]) -> str:
        """
        지원 형식:

        INFO memory
        """
        if len(args) != 2:
            return self._wrong_arguments("INFO")

        section = args[1].lower()

        if section != "memory":
            return (
                "(error) ERR unsupported INFO section "
                f"'{args[1]}'"
            )

        memory_info = self.redis.info_memory()

        return (
            f"used_memory:{memory_info.used_memory}\n"
            f"maxmemory:{memory_info.maxmemory}\n"
            f"evicted_keys:{memory_info.evicted_keys}"
        )

    def _wrong_arguments(self, command: str) -> str:
        return (
            "(error) ERR wrong number of arguments "
            f"for '{command.lower()}' command"
        )

    def _invalid_integer(self) -> str:
        return (
            "(error) ERR value is not an integer "
            "or out of range"
        )