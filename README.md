# Collector agent

[![made-with-python](https://img.shields.io/badge/Made%20with-Python%203.10-1f425f.svg?logo=python)](https://www.python.org/)
[![GitHub](https://img.shields.io/github/license/StrangeAlbatros/collector-agent?style=flat)](https://github.com/StrangeAlbatros/collector-agent/blob/main/LICENSE)

---
# Table of content

[1. What is collector-agent](#1-what-is-collector-agent)

[2. Installation](#2-installation)

[3. Using](#3-using)

[4. Support](#4-support)

---

## 1. What is collector-agent

**Collector agent** is a piece of software that is installed on a target computer and used to collect data about the system. This data may include information about services, installed packages, and network information. The collector agent is used to monitor and analyze system performance, as well as detect and prevent security threats.

## 2. Installation

You need to **python** for running this collector

Install requirement

```bash
pip3 install -r requirements.txt
```

## 3. Using

```
python3 __main__.py
```

## 4. Support

### Python

You need at least python version `3.5`

### OS

| OS          | Version |
|-------------|---------|
| Debian like |   >=9   |
| MacOSX      |         |
| Windows     |  >=10   |

### Features

| Feature     | Debian like |MacOSX|Windows|
|-------------|-------------|------|-------|
| Installed packages| :white_check_mark: |:white_check_mark:|:white_check_mark:|
| Services| :white_check_mark: |:white_check_mark:|:white_check_mark:|
| Network information| :white_check_mark: |:white_check_mark:||

### Debian like

- Installl packages: dpkg (``` dpkg -l ```)
- Services: systemctl (``` systemctl --type=service --state=running ```)
- Networks informations

### Windows

- Installl packages: (``` Get-Package ```)
- Services: (``` sc queryex type=service ```)
- Networks informations

### MacOS X

- Installl packages:
    - pkgutil (``` pkgutil --pkgs ```)
    - brew (``` brew list ```)
- Services:
    - launchctl (``` launchctl list ```)
    - brew (``` brew services list ```)
- Networks informations