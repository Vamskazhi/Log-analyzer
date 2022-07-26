from steps import find_log_file

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}

find_log_file(log_dir=config['LOG_DIR'])