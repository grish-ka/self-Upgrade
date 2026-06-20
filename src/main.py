import argparse
import sys
from loguru import logger
import requests

version = "v0.1.2"

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
    check_update()

    program(args)

@logger.catch(level="WARNING")
def check_update(): 
    username = "grish-ka"
    repo = "self-Update"
    latest_release_url = f"https://api.github.com/repos/{username}/{repo}/releases/latest"
    response = requests.get(latest_release_url)
    if response.status_code != 200:
        logger.error("Failed to fetch latest release information.")
        logger.debug(f"Response status code: {response.status_code}, Response text: {response.text}")
        return
    release_data = response.json()
    logger.debug(release_data)
    latest_version = release_data["tag_name"]
    logger.debug(f"Latest version: {latest_version}, Current version: {version}")

    if latest_version != version:
        logger.opt(colors=True).warning(f"New version available: <green>{latest_version}</green>. Current version: <red>{version}</red>.")
    else:
        logger.debug(f"You are using the latest version: {version}.")

def program(args):
    logger.opt(colors=True).info(f"TEXT: <blue>{args.text}</blue>")

if __name__ == "__main__":
    main()