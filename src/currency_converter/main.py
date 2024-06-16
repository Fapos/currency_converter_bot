import argparse
import asyncio

from typing import Any
from bot import *


def main(prog: str = None, args: Any = None):
    parser = argparse.ArgumentParser(
        prog=prog,
        description='Telegram currency converter bot',
    )

    parser.add_argument('-c', '--config')
    _args = parser.parse_args()
    bot = Bot(Path(_args.config))
    asyncio.run(bot.start())


if __name__ == '__main__':
    main()
