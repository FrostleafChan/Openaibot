# -*- coding: utf-8 -*-
# @Time    : 2023/10/18 下午10:23
import getopt
import os
import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv()
logger.remove(0)
handler_id = logger.add(
    sys.stderr,
    format="<level>[{level}]</level> | <level>{message}</level> | <yellow>@{time}</yellow>",
    colorize=True,
    backtrace=True,
    enqueue=True,
    level="DEBUG" if os.getenv("DEBUG", None) else "INFO",
)
logger.add(
    sink="receiver.log",
    format="<level>[{level}]</level> | <level>{message}</level> | <yellow>@{time}</yellow>",
    level="DEBUG",
    rotation="100 MB",
    enqueue=True,
)
head = """
██╗     ██╗     ███╗   ███╗██╗  ██╗██╗██████╗  █████╗
██║     ██║     ████╗ ████║██║ ██╔╝██║██╔══██╗██╔══██╗
██║     ██║     ██╔████╔██║█████╔╝ ██║██████╔╝███████║
██║     ██║     ██║╚██╔╝██║██╔═██╗ ██║██╔══██╗██╔══██║
███████╗███████╗██║ ╚═╝ ██║██║  ██╗██║██║  ██║██║  ██║
╚══════╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
"""
logger.opt(record=False, exception=False, capture=False, colors=True).info(
    f"<cyan>{head}</cyan>"
)

# Log System
if os.getenv("SENTRY_DSN", None):
    try:
        import sentry_sdk

        sentry_sdk.init(
            dsn=os.getenv("SENTRY_DSN"),
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
    except Exception as e:
        logger.error(f"SENTRY ERROR: {e}")
    else:
        logger.success("🌟 Create Sentry Client Successfully!")

# Tutorial
SKIP_TUTORIAL = False
SKIP_EXISTING = True
opts, args = getopt.getopt(sys.argv[1:], "h", ["no_tutorial", "tutorial"])
for op, value in opts:
    if op == "--no_tutorial":  # 获取命令行参数的 --no_tutorial
        SKIP_TUTORIAL = True
    if op == "-h":
        print("Usage: python start_receiver.py [--no_tutorial] [--tutorial]")
        sys.exit()
    if op == "--tutorial":
        SKIP_EXISTING = False
if not SKIP_TUTORIAL:
    from app.tutorial import show_tutorial

    show_tutorial(skip_existing=SKIP_EXISTING, pre_step_stop=4, database_key="01")

# Run Receiver
from app.receiver import app  # noqa

app.run()
