# desktop_main_csv.py
import sys, os
from streamlit.web import bootstrap

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(here, "app_desktop_csv.py")
    sys.argv = ["streamlit", "run", app_path, "--server.headless=false", "--browser.gatherUsageStats=false"]
    bootstrap.load_config_options(flag_options={})
    bootstrap.run(app_path, False, [], {})

if __name__ == "__main__":
    main()
