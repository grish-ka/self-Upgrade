from loguru import logger
import requests

@logger.catch(level="WARNING")
def check_update(username, repo, version): 

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

