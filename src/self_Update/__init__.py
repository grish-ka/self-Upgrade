from loguru import logger
import requests
from packaging import version # Run: pip install packaging


@logger.catch(level="WARNING")
def check_update(username, repo, version): 
    latest_release_url = f"https://api.github.com/repos/{username}/{repo}/releases/latest"
    
    try:
        # Added a 5-second timeout so the tool never freezes
        response = requests.get(latest_release_url, timeout=5)
        response.raise_for_status() # Automatically flags 404s, 403 rate limits, etc.
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch latest release information.")
        logger.debug(f"Network error details: {e}")
        return False, None

    release_data = response.json()
    latest_version_str = release_data.get("tag_name", "")
    
    logger.debug(f"Latest version: {latest_version_str}, Current version: {version}")

    try:
        # Strip 'v' prefixes to ensure a clean math comparison (e.g., 'v1.2.3' -> '1.2.3')
        clean_latest = latest_version_str.lstrip('v')
        clean_current = version.lstrip('v')
        
        # The Magic: True mathematical version comparison
        if version.parse(clean_latest) > version.parse(clean_current):
            logger.opt(colors=True).warning(
                f"New version available: <green>{latest_version_str}</green>. "
                f"Current version: <red>{version}</red>."
            )
        else:
            logger.debug(f"You are using the latest version: {version}.")
            
    except version.InvalidVersion:
        logger.warning(f"Could not parse version strings for comparison (Latest: {latest_version_str}, Current: {version})")
        return False, None


@logger.catch(level="WARNING")
def check_update_base(username: str, repo: str, version: str): 
    latest_release_url = f"https://api.github.com/repos/{username}/{repo}/releases/latest"
    
    try:
        # Added a 5-second timeout so the tool never freezes
        response = requests.get(latest_release_url, timeout=5)
        response.raise_for_status() # Automatically flags 404s, 403 rate limits, etc.
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch latest release information.")
        logger.debug(f"Network error details: {e}")
        return False, None

    release_data = response.json()
    latest_version_str = release_data.get("tag_name", "")
    
    logger.debug(f"Latest version: {latest_version_str}, Current version: {version}")

    try:
        # Strip 'v' prefixes to ensure a clean math comparison (e.g., 'v1.2.3' -> '1.2.3')
        clean_latest = latest_version_str.lstrip('v')
        clean_current = version.lstrip('v')
        
        # The Magic: True mathematical version comparison
        if version.parse(clean_latest) > version.parse(clean_current):
            logger.opt(colors=True).debug(
                f"New version available: <green>{latest_version_str}</green>. "
                f"Current version: <red>{version}</red>."
            )
            return True, latest_version_str # True = Update Needed!
        else:
            logger.debug(f"You are using the latest version: {version}.")
            return False, latest_version_str # False = You are good to go!
            
    except version.InvalidVersion:
        logger.warning(f"Could not parse version strings for comparison (Latest: {latest_version_str}, Current: {version})")
        return False, None