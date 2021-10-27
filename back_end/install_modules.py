import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    install("flask")
    install("flask_cors")
    # install("urllib.request")
    # install("ntpath")
    # install("json")
    # install("time")
    # install("io")
    # install("base64")
    install("requests")
    # install("os")
    # install("sys")
    # install("cv2")
    install("numpy")
    # install("matplotlib.pyplot")
    # install("PIL")

if __name__ == "__main__":
    main()