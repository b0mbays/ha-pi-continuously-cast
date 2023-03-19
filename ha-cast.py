import subprocess
import time
import logging
import logging.handlers

from logging.handlers import RotatingFileHandler

log_file = "ha-cast.log"
max_log_size = 10 * 1024 * 1024  # 10 MB
max_log_files = 5

handler = logging.handlers.RotatingFileHandler(
    log_file,
    maxBytes=max_log_size,
    backupCount=max_log_files,
)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logging.basicConfig(level=logging.INFO, handlers=[handler])

#Change the following for your own device(s)
device_map = {
    "<DEVICE_1_NAME>": "<DEVICE_1_DASHBOARD>",
    "<DEVICE_2_NAME>": "<DEVICE_2_DASHBOARD>",
    "<DEVICE_3_NAME>": "<DEVICE_3_DASHBOARD>",
}

def check_dashboard_state(device_name):
    try:
        status_output = subprocess.check_output(["catt", "-d", device_name, "status"]).decode()
        if "Dummy" in status_output:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking dashboard state for {device_name}: {e}")
        return None

def check_media_state(device_name):
    try:
        status_output = subprocess.check_output(["catt", "-d", device_name, "status"]).decode()
        if "PLAYING" in status_output:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking media state for {device_name}: {e}")
        return None

def check_both_states(device_name):
    try:
        if check_dashboard_state(device_name) or check_media_state(device_name):
            return True
        return False
    except TypeError:
        return None

def cast_dashboard(device_name, dashboard_url):
    try:
        logging.info(f"Casting dashboard to {device_name}")
        subprocess.call(["catt", "-d", device_name, "stop"])
        subprocess.call(["catt", "-d", device_name, "volume", "0"])
        subprocess.call(["catt", "-d", device_name, "cast_site", dashboard_url])
        subprocess.call(["catt", "-d", device_name, "volume", "50"])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error casting dashboard to {device_name}: {e}")
        return None

# loop continuously check the media and dashboard state and cast the dashboard only if necessary
max_retries = 5
retry_delay = 30
retry_count = 0

while True:
    for device_name, dashboard_url in device_map.items():
        retry_count = 0
        while retry_count < max_retries:
            if check_both_states(device_name) is None:
                retry_count += 1
                logging.warning(f"Retrying in {retry_delay} seconds for {retry_count} time(s) due to previous errors")
                time.sleep(retry_delay)
                continue
            elif check_both_states(device_name):
                logging.info(f"HA Dashboard (or media) is playing on {device_name}...")
            else:
                logging.info(f"HA Dashboard (or media) is NOT playing on {device_name}!")
                cast_dashboard(device_name, dashboard_url)
            break
        else:
            logging.error(f"Max retries exceeded for {device_name}. Skipping...")
            continue
    time.sleep(20)
