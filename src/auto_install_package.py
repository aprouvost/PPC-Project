#!/usr/bin/env python

import os


def autoInstall():
    print("----------------------------\n"
          "Checking insatallation module\n"
          "----------------------------\n")
    try:
        import pip
    except ModuleNotFoundError:
        print("----------------------------\n"
              "Installation of pip is needed,\n"
              "use your admin password to install\n"
              "with apt command\n"
              "----------------------------\n")
        os.system("sudo apt update")
        os.system("sudo apt install -y python3-pip")

    pkgs = ['termcolor', 'sysv_ipc', 'pynput']
    for package in pkgs:
        try:
            import package
        except ImportError as e:
            os.system("pip3 install " + package)
