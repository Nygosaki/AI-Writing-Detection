# coding: utf-8
import os
import re
import shutil
import subprocess
import sys
import platform as pf
from packaging import version


def get_chromedriver_filename():
    """
    Returns the filename of the binary for the current platform.
    :return: Binary filename
    """
    if sys.platform.startswith("win"):
        return "chromedriver.exe"
    return "chromedriver"


def get_variable_separator():
    """
    Returns the environment variable separator for the current platform.
    :return: Environment variable separator
    """
    if sys.platform.startswith("win"):
        return ";"
    return ":"


def get_platform_architecture(chrome_version=None):
    if sys.platform.startswith("linux") and sys.maxsize > 2**32:
        platform = "linux"
        architecture = "64"
    elif sys.platform == "darwin":
        platform = "mac"
        # At some points, the release naming for Apple arm changed;
        # Looking in http://chromedriver.storage.googleapis.com/, the changeover happened across these releases:
        # 106.0.5249.61/chromedriver_mac_arm64.zip
        # 106.0.5249.21/chromedriver_mac64_m1.zip
        # Mac architecture naming changed again as of the transition to CfT
        # 115.0.5763.0/mac-arm64/chromedriver-mac-arm64.zip'
        # 115.0.5763.0/mac-x64/chromedriver-mac-x64.zip'
        
        if pf.processor() == "arm":
            if chrome_version is not None and get_major_version(chrome_version) >= "115":
                print("CHROME >= 115, using mac-arm64 as architecture identifier")
                architecture = "-arm64"
            elif chrome_version is not None and version.parse(chrome_version) <= version.parse("106.0.5249.21"):
                print("CHROME <= 106.0.5249.21, using mac64_m1 as architecture identifier")
                architecture = "64_m1"
            else:
                architecture = "_arm64"
        elif pf.processor() == "i386":
            if chrome_version is not None and get_major_version(chrome_version) >= "115":
                print("CHROME >= 115, using mac-x64 as architecture identifier")
                architecture = "-x64"
            else:
                architecture = "64"
        else:
            raise RuntimeError("Could not determine Mac processor architecture.")
    elif sys.platform.startswith("win"):
        platform = "win"
        architecture = "32"
    else:
        raise RuntimeError(
            "Could not determine chromedriver download URL for this platform."
        )
    return platform, architecture


def get_chromedriver_url(chromedriver_version, download_options, no_ssl=False):
    """
    Generates the download URL for current platform , architecture and the given version.
    Supports Linux, MacOS and Windows.

    :param chromedriver_version: ChromeDriver version string
    :param no_ssl:               Whether to use the encryption protocol when downloading the chrome driver
    :return:                     String. Download URL for chromedriver
    """
    platform, architecture = get_platform_architecture(chromedriver_version)
    if get_major_version(chromedriver_version) >= "115":  # new CfT ChromeDriver versions have their URLs published, so we already have a list of options
        for option in download_options:
            if option["platform"] == platform + architecture:
                        return option['url']
    else:  # old ChromeDriver versions use the old urls
        base_url = "chromedriver.storage.googleapis.com/"
        base_url = "http://" + base_url if no_ssl else "https://" + base_url
        return base_url + chromedriver_version + "/chromedriver_" + platform + architecture + ".zip"


def find_binary_in_path(filename):
    """
    Searches for a binary named `filename` in the current PATH. If an executable is found, its absolute path is returned
    else None.
    :param filename: Filename of the binary
    :return: Absolute path or None
    """
    if "PATH" not in os.environ:
        return None
    for directory in os.environ["PATH"].split(get_variable_separator()):
        binary = os.path.abspath(os.path.join(directory, filename))
        if os.path.isfile(binary) and os.access(binary, os.X_OK):
            return binary
    return None


def check_version(binary, required_version):
    try:
        version = subprocess.check_output([binary, "-v"])
        version = re.match(r".*?([\d.]+).*?", version.decode("utf-8"))[1]
        if version == required_version:
            return True
    except Exception:
        return False
    return False


def get_chrome_version():
    """
    :return: the version of chrome installed on client
    """
    platform, _ = get_platform_architecture()
    if platform == "linux":
        path = get_linux_executable_path()
        with subprocess.Popen([path, "--version"], stdout=subprocess.PIPE) as proc:
            version = (
                proc.stdout.read()
                .decode("utf-8")
                .replace("Chromium", "")
                .replace("Google Chrome", "")
                .strip()
            )
    elif platform == "mac":
        process = subprocess.Popen(
            [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "--version",
            ],
            stdout=subprocess.PIPE,
        )
        version = (
            process.communicate()[0]
            .decode("UTF-8")
            .replace("Google Chrome", "")
            .strip()
        )
    elif platform == "win":
        PROGRAMFILES = f"{os.environ.get('PROGRAMW6432') or os.environ.get('PROGRAMFILES')}\\Google\\Chrome\\Application"
        PROGRAMFILESX86 = f"{os.environ.get('PROGRAMFILES(X86)')}\\Google\\Chrome\\Application"
        
        path = PROGRAMFILES if os.path.exists(PROGRAMFILES) else PROGRAMFILESX86 if os.path.exists(PROGRAMFILESX86) else None

        dirs = [f.name for f in os.scandir(path) if f.is_dir() and re.match("^[0-9.]+$", f.name)] if path else None

        version = max(dirs) if dirs else None
    else:
        return
    return version


def get_linux_executable_path():
    """
    Look through a list of candidates for Google Chrome executables that might
    exist, and return the full path to first one that does. Raise a ValueError
    if none do.

    :return: the full path to a Chrome executable on the system
    """
    for executable in (
        "google-chrome",
        "google-chrome-stable",
        "google-chrome-beta",
        "google-chrome-dev",
        "chromium-browser",
        "chromium",
    ):
        path = shutil.which(executable)
        if path is not None:
            return path
    raise ValueError("No chrome executable found on PATH")


def get_major_version(version):
    """
    :param version: the version of chrome
    :return: the major version of chrome
    """
    return version.split(".")[0]

if __name__ == "__main__":
    print(get_chrome_version())
  