import argparse
import sys
from loguru import logger
from . import check_update

version = "v26.2.0.1"

@logger.catch()
def main():
    logger.remove()
    logger.add("./logs/self-Update_{time}.log", level="INFO", retention="1 days", rotation="500 MB", compression="zip")
    logger.add(sys.stdout, level="INFO")       
    parser = argparse.ArgumentParser(prog="self-Update", description="Update itself")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--version", action="version", version=version)
    parser.add_argument("--text", "-t", type=str, help="Text to display", default="Hello, World!")
    args = parser.parse_args()

    # Your update logic here
    if args.verbose:
        logger.remove()
        logger.add("./logs/self-Update_{time}.log", level="DEBUG", retention="1 days", rotation="500 MB", compression="zip")
        logger.add(sys.stdout, level="DEBUG")


    logger.info("System loaded successfully.")

    # update logic
    check_update("grish-ka", "self-Update", version)

    program(args)



def program(args):
    logger.opt(colors=True).info(f"TEXT: <blue>{args.text}</blue>")

if __name__ == "__main__":
    main()