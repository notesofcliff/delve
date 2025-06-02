# Copyright (C) 2025 All rights reserved.
# This file is part of the Delve project, which is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the root of this repository for details.

import sys
import shutil
import hashlib
import logging
import argparse
import platform as _platform
import subprocess
import logging.config
from pathlib import Path
from time import  sleep
import requests

ERRORS = {
    'UNSUPPORTED_PLATFORM': 1,
    'AMBIGUOUS_INSTALL': 2,
    'HASH_MISMATCH': 3,
}

HERE = Path(__file__).parent

cli = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
cli.add_argument(
    "-p",
    "--python-version",
    help="The version of cPython to target. (i.e. 3.13.3)",
    default="3.13.3",
)
cli.add_argument(
    "--hash-buff-size",
    help="The buffer size for reads when calculating hashes",
    default=65536,
)
cli.add_argument(
    "--build-directory",
    help="The directory to use for downloads and other file "
         "operations, WARNING: This directory will be deleted "
         "before any work is done on the build.",
    type=Path,
    default=HERE.joinpath("build"),
)
cli.add_argument(
    "--dist-directory",
    help="The directory to store the distributable artifacts "
         "WARNING: This directory will be deleted",
    type=Path,
    default=HERE.joinpath("dist"),
)
cli.add_argument(
    "--src-directory",
    help="The directory where the projects source code resides.",
    type=Path,
    default=HERE.joinpath("src")
)
cli.add_argument(
    "--log-level",
    help="The level (0-50) at which to filter log levels (lower is more verbose)",
    default=30,
    type=int,
)
cli.add_argument(
    "--npx-executable",
    help="npx with webpack installed is required to run this build script "
         "default is to assume npx is on the PATH",
    default="npx"
)
cli.add_argument(
    "--npm-executable",
    help="npm is required to run this build script "
         "default is to assume npm is on the PATH",
    default="npm"
)
cli.add_argument(
    "--clean-only",
    help="Clean up build artifacts and exit",
    action="store_true",
)
args = cli.parse_args()

TARGET_PYTHON_VERSION = args.python_version
HASH_BUFF_SIZE = args.hash_buff_size

BUILD_DIRECTORY = args.build_directory
shutil.rmtree(BUILD_DIRECTORY, ignore_errors=True)

ASSEMBLE_DIRECTORY = BUILD_DIRECTORY.joinpath('assemble')
shutil.rmtree(ASSEMBLE_DIRECTORY, ignore_errors=True)

DIST_DIRECTORY = args.dist_directory
shutil.rmtree(DIST_DIRECTORY, ignore_errors=True)

SRC_DIRECTORY = args.src_directory
HOME_DIRECTORY = SRC_DIRECTORY.joinpath('home')

for p in HOME_DIRECTORY.glob("**/__pycache__"):
    shutil.rmtree(p)

if HOME_DIRECTORY.joinpath("db.sqlite3").exists():
    HOME_DIRECTORY.joinpath("db.sqlite3").unlink()

if HOME_DIRECTORY.joinpath(".venv").exists():
    shutil.rmtree(HOME_DIRECTORY.joinpath(".venv"))

for p in HOME_DIRECTORY.glob("staticfiles/*"):
    if p.name == ".empty":
        pass
    elif p.is_file():
        p.unlink()
    elif p.is_dir():
        shutil.rmtree(p)

if HERE.joinpath("build.log").exists():
    HERE.joinpath("build.log").unlink()
if HERE.joinpath("node_modules").exists():
    shutil.rmtree(HERE.joinpath("node_modules"))
for p in HOME_DIRECTORY.joinpath("log").glob("*.log"):
    if p.name == ".empty":
        pass
    p.unlink()
    
if args.clean_only:
    sys.exit(0)

BUILD_DIRECTORY.mkdir()
ASSEMBLE_DIRECTORY.mkdir()
DIST_DIRECTORY.mkdir()

INVOCATION_SCRIPTS_DIRECTORY = HOME_DIRECTORY.joinpath('invocation_scripts')
STATIC_ASSETS_DIRECTORY = HOME_DIRECTORY.joinpath('static_assets')

NPX_EXECUTABLE = args.npx_executable
NPM_EXECUTABLE = args.npm_executable

# Clean up any development cruft

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(levelname)-8s: %(asctime)s: %(message)s"
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "level": args.log_level,
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "simple",
                "level": args.log_level,
                "filename": HERE.joinpath('build.log'),
                "mode": "w"
            }
        },
        "root": {
            "level": args.log_level,
            "handlers": [
                "stdout",
                "file"
            ]
        }
    }
)
log = logging.getLogger(__name__)

def fail_for_unsupported_platform(platform):
    log.critical(f"Unable to continue due to unsupported platform: {platform}")
    sys.exit(ERRORS['UNSUPPORTED_PLATFORM'])

def fail_for_ambiguity(release_names):
    log.critical(f"Unable to determine correct Python build out of: {', '.join(release_names)}")
    sys.exit(ERRORS['AMBIGUOUS_INSTALL'])

def fail_for_hash_mismatch(expected, actual):
    log.critical(f"Unable to continue. Release file does not match hash. Expected: '{expected}', Actual: '{actual}'")
    sys.exit(ERRORS['HASH_MISMATCH'])

def get_file_sha256(p):
    sha256 = hashlib.sha256()
    with p.open('rb') as fp:
        while True:
            data = fp.read(HASH_BUFF_SIZE)
            if not data:
                break
            else:
                sha256.update(data)
    return sha256.hexdigest()

platform = sys.platform
if platform.startswith('linux'):
    log.debug(f"Found Linux platform: {platform}")
    platform = 'linux'
elif platform.startswith('win32'):
    log.debug(f"Found Windows platform: {platform}")
    platform = 'windows'
elif platform.startswith('darwin'):
    log.debug(f"Found MacOS platform: {platform}")
    platform = 'darwin'
# The elifs here are strictly here for documentation if we need to
# support these platforms in the future
elif platform.startswith('freebsd'):
    fail_for_unsupported_platform(platform)
elif platform.startswith('aix'):
    fail_for_unsupported_platform(platform)
elif platform.startswith('emscripten'):
    fail_for_unsupported_platform(platform)
elif platform.startswith('wasi'):
    fail_for_unsupported_platform(platform)
elif platform.startswith('cygwin'):
    fail_for_unsupported_platform(platform)
else:
    fail_for_unsupported_platform(platform)

requirements_file = HERE.joinpath(f'{platform}-requirements.txt')
log.debug(f"Found requirements_file: {requirements_file}")

# Download a prebuilt Python distribution
# First, get the latest release tag
response = requests.get(
    'https://raw.githubusercontent.com/indygreg/python-build-standalone/latest-release/latest-release.json',
)
response_json = response.json()
log.debug(f"Found response json: {response_json}")
tag = response_json['tag']
log.debug(f"Found tag: {tag}")

# Second, Get the release ID from Github API
response = requests.get(
    f'https://api.github.com/repos/indygreg/python-build-standalone/releases/tags/{tag}',
    headers={
        'X-GitHub-Api-Version': '2022-11-28',
        'Accept': 'application/vnd.github+json'
    }
)
response_json = response.json()
# log.debug(f"Found response json: {response_json}")
assets = response_json['assets']
# log.debug(f"Found assets: {assets}")
release_names = [d['name'] for d in assets]
# log.debug(f"Found release_names: {release_names}")
# Filter to install_only build configuration
release_names = [name for name in release_names if 'install_only_stripped' in name]
# log.debug(f"Found 'install_only_stripped' release_names: {release_names}")
# Filter to only the python version that we are interested in
release_names = [name for name in release_names if TARGET_PYTHON_VERSION in name]
log.debug(f"Found correct python version release_names: {release_names}")
# Filter to only platform and architecture that we are interested in
if platform == 'windows':
    release_names = [name for name in release_names if 'windows-msvc' in name]
elif platform == 'linux':
    release_names = [name for name in release_names if 'unknown-linux-gnu' in name]
elif platform == 'darwin':
    release_names = [name for name in release_names if 'apple-darwin' in name]

log.debug(f"Found platform specific release_names: {release_names}")

# Filter to only bitness that we are interested in
if platform == "windows":
    if sys.maxsize > 2**32:
        release_names = [name for name in release_names if 'x86_64' in name]
    else:
        release_names = [name for name in release_names if 'i686' in name]
elif platform == "linux":
    if sys.maxsize > 2**32:
        release_names = [name for name in release_names if 'x86_64' in name]
        release_names = [name for name in release_names if 'x86_64_v2' not in name]
        release_names = [name for name in release_names if 'x86_64_v3' not in name]
        release_names = [name for name in release_names if 'x86_64_v4' not in name]
    else:
        release_names = [name for name in release_names if 'i686' in name]
elif platform == "darwin":
    if _platform.machine() == "x86_64":
        release_names = [name for name in release_names if 'x86_64' in name]
    elif _platform.machine() == "arm64":
        release_names = [name for name in release_names if 'aarch64' in name]
log.debug(f"Found bitness-correct release_names: {release_names}")

# There should be two: one for the hash and one for the actual release
if len(release_names) > 2:
    fail_for_ambiguity(release_names)

# Third, find the release file and the hash file
for name in release_names:
    if name.endswith('sha256'):
        hash_file = name
    else:
        release_file = name

log.debug(f'Found hash_file: {hash_file}')
log.debug(f'Found release_file: {release_file}')

# Pull out the url for the assets we identified
for asset in assets:
    if asset['name'] == hash_file:
        # get url for hash_file
        hash_file_url = asset['url']
    elif asset['name'] == release_file:
        # get url for release_file
        release_file_url = asset['url']

log.debug(f'Found hash_file_url: {hash_file_url}')
log.debug(f'Found release_file_url: {release_file_url}')

# Fourth Download Hash file
hash_file_response = requests.get(
    hash_file_url,
    headers={
        'X-GitHub-Api-Version': '2022-11-28',
        'Accept': 'application/octet-stream'
    }
)
hash_file_path = BUILD_DIRECTORY.joinpath(hash_file)
with hash_file_path.open('wb') as fp:
    fp.write(hash_file_response.content)
hash_hex = hash_file_path.read_text().strip()
log.debug(hash_hex)

# Fifth Download Release file
release_file_response = requests.get(
    release_file_url,
    headers={
        'X-GitHub-Api-Version': '2022-11-28',
        'Accept': 'application/octet-stream'
    }
)
release_file_path = BUILD_DIRECTORY.joinpath(release_file)
with release_file_path.open('wb') as fp:
    fp.write(release_file_response.content)

# Verify the hash of the downloaded release file
release_file_sha256 = get_file_sha256(release_file_path)
if hash_hex != release_file_sha256:
    fail_for_hash_mismatch(hash_hex, release_file_sha256)
else:
    log.info("Downloaded Python release matches expected hash value")

# Extract the release file into the dist directory
shutil.unpack_archive(
    release_file_path,
    ASSEMBLE_DIRECTORY,
)

# Move everything under python directory into subdirectory based on python version
src_dir = ASSEMBLE_DIRECTORY.joinpath('python')
dst_dir = src_dir.joinpath(TARGET_PYTHON_VERSION)
for item in src_dir.iterdir():
    if item != dst_dir:
        shutil.move(item, dst_dir.joinpath(item.name))

if platform == "windows":
    python_executable = ASSEMBLE_DIRECTORY.joinpath('python').joinpath(TARGET_PYTHON_VERSION).joinpath('python')
else:
    python_executable = ASSEMBLE_DIRECTORY.joinpath('python').joinpath(TARGET_PYTHON_VERSION).joinpath('bin').joinpath('python3')

# Upgrade pip
command = f'{python_executable} -m pip install --upgrade pip'
subprocess.run(command, shell=True)

# Install dependencies
command = f'{python_executable} -m pip install --no-warn-script-location -r {requirements_file}'
subprocess.run(command, shell=True)

# Collect staticfiles
command = f'{python_executable} {HOME_DIRECTORY.joinpath("manage.py")} collectstatic --no-input'
subprocess.run(command, shell=True)

# Install node/npm
command = f"{NPM_EXECUTABLE} install"
subprocess.run(command, shell=True)

# Bundle custom js and css
command = f'{NPX_EXECUTABLE} webpack --config {HERE.joinpath("webpack.config.js")}'
subprocess.run(command, shell=True)

command = f'{NPX_EXECUTABLE} webpack --config {HERE.joinpath("fltable-webpack.config.js")}'
subprocess.run(command, shell=True)

command = f'{NPX_EXECUTABLE} webpack --config {HERE.joinpath("flchart-webpack.config.js")}'
subprocess.run(command, shell=True)

# command = f'{NPX_EXECUTABLE} webpack --config {HERE.joinpath("search-webpack.config.js")}'
# subprocess.run(command, shell=True)

JS_DIRECTORY = HOME_DIRECTORY.joinpath("staticfiles").joinpath("js")
if not JS_DIRECTORY.exists():
    JS_DIRECTORY.mkdir()
for p in DIST_DIRECTORY.glob("staticfiles/*"):
    shutil.copy(p, JS_DIRECTORY)

CSS_DIRECTORY = HOME_DIRECTORY.joinpath("staticfiles").joinpath("css")
if not CSS_DIRECTORY.exists():
    CSS_DIRECTORY.mkdir()
shutil.copy(DIST_DIRECTORY.joinpath("main.css"), CSS_DIRECTORY.joinpath("main.css"))
for p in DIST_DIRECTORY.glob("*.woff*"):
    shutil.copy(p, CSS_DIRECTORY)


# Copy all files from src/home
for item in HOME_DIRECTORY.iterdir():
    if item.is_dir():
        shutil.copytree(
            item,
            ASSEMBLE_DIRECTORY.joinpath(item.name),
        )
    else:
        shutil.copy(
            item,
            ASSEMBLE_DIRECTORY.joinpath(item.name),
        )

# Rename settings file, so we don't overwrite user settings if they are updating in-place
ASSEMBLE_DIRECTORY.joinpath("delve").joinpath("settings.py").rename(
    ASSEMBLE_DIRECTORY.joinpath("delve").joinpath("example-settings.py")
)
ASSEMBLE_DIRECTORY.joinpath("delve").joinpath("urls.py").rename(
    ASSEMBLE_DIRECTORY.joinpath("delve").joinpath("example-urls.py")
)

# Copy all invocation scripts from src/invocation_scripts/{platform} to DIST_DIRECTORY
script_dir = SRC_DIRECTORY.joinpath('invocation_scripts').joinpath(platform)
for item in script_dir.iterdir():
    if item.name.startswith('set-env'):
        contents = item.read_text()
        contents = contents.replace('{PYTHON_VERSION}', TARGET_PYTHON_VERSION)
        file_path = ASSEMBLE_DIRECTORY.joinpath(item.name)
        file_path.write_text(contents)
    else:
        file_path = ASSEMBLE_DIRECTORY.joinpath(item.name)
        shutil.copy(item, file_path)
    if platform.lower() != "windows":
        file_path.chmod(0o750)
command = f'{python_executable} {ASSEMBLE_DIRECTORY}/manage.py version'
output = subprocess.check_output(command, shell=True)
flashligt_version = output.strip().decode()

# Generate a versioned requirements.txt file
versioned_requirements_file = ASSEMBLE_DIRECTORY.joinpath(f'delve-{flashligt_version}_{requirements_file.name}')
shutil.copy(requirements_file, versioned_requirements_file)

# Clean up any __pycache__ directories in the source code-only directory
for p in ASSEMBLE_DIRECTORY.glob("**/__pycache__"):
    log.debug(f"Removing: {p}")
    shutil.rmtree(p)

# Clean up any .pyc files in the source code-only directory
# for p in ASSEMBLE_DIRECTORY.glob("**/*.pyc"):
#     log.debug(f"Removing: {p}")
#     p.unlink()

# # Clean up any .pyo files in the source code-only directory
# for p in ASSEMBLE_DIRECTORY.glob("**/*.pyo"):
#     log.debug(f"Removing: {p}")
#     p.unlink()

# # Clean up any .pyd files in the source code-only directory
# for p in ASSEMBLE_DIRECTORY.glob("**/*.pyd"):
#     log.debug(f"Removing: {p}")
#     p.unlink()

# clean up log files
for p in ASSEMBLE_DIRECTORY.glob("**/*.log"):
    log.debug(f"Removing: {p}")
    p.unlink()

shutil.make_archive(
    DIST_DIRECTORY.joinpath(
        f'DELVE-{flashligt_version}_py{TARGET_PYTHON_VERSION}_{platform}_install',
    ),
    format='zip',
    root_dir=ASSEMBLE_DIRECTORY,
    base_dir='.',
)


# Rename SRC_ONLY_DIRECTORY to UPDATE_PACKAGE_DIRECTORY
UPDATE_PACKAGE_DIRECTORY = BUILD_DIRECTORY.joinpath('update_package')
shutil.rmtree(UPDATE_PACKAGE_DIRECTORY, ignore_errors=True)

# Copy ASSEMBLE_DIRECTORY to UPDATE_PACKAGE_DIRECTORY
shutil.copytree(ASSEMBLE_DIRECTORY, UPDATE_PACKAGE_DIRECTORY)

# Remove the python subdirectory from the update package
sleep(5)
python_subdir = UPDATE_PACKAGE_DIRECTORY.joinpath('python')
if python_subdir.exists():
    shutil.rmtree(python_subdir)

# Clean up any __pycache__ directories in the update package
for p in UPDATE_PACKAGE_DIRECTORY.glob("**/__pycache__"):
    log.debug(f"Removing: {p}")
    shutil.rmtree(p)

# Clean up any .pyc files in the update package
# for p in UPDATE_PACKAGE_DIRECTORY.glob("**/*.pyc"):
#     log.debug(f"Removing: {p}")
#     p.unlink()

# Clean up any .pyo files in the update package
# for p in UPDATE_PACKAGE_DIRECTORY.glob("**/*.pyo"):
#     log.debug(f"Removing: {p}")
#     p.unlink()

# Clean up any .pyd files in the update package
# for p in UPDATE_PACKAGE_DIRECTORY.glob("**/*.pyd"):
#     log.debug(f"Removing: {p}")
#     p.unlink()

# Clean up log files in the update package
for p in UPDATE_PACKAGE_DIRECTORY.glob("**/*.log"):
    log.debug(f"Removing: {p}")
    p.unlink()

# Create a zip archive from the update package directory
shutil.make_archive(
    DIST_DIRECTORY.joinpath(
        f'DELVE-{flashligt_version}_py{TARGET_PYTHON_VERSION}_{platform}_update',
    ),
    format='zip',
    root_dir=UPDATE_PACKAGE_DIRECTORY,
    base_dir='.',
)
