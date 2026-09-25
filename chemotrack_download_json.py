#!/usr/bin/env python3

from pathlib import Path
import subprocess

###########################################################################
# Configuration
###########################################################################

## please check the domain name from the Bioimage Archive website
## they change it sometimes and you need to paste the correct name below (case sensitive)
REMOTE_ROOT = (
    "ftp://ftp.ebi.ac.uk/biostudies/fire/S-BIAD/674/S-BIAD3674/Files/ChemoTrack"
)

# replace this with a local directory in your PC
LOCAL_ROOT = Path(
    "/media/devi/New Volume/ChemoTrack_download"
)

###########################################################################
# Conditions
###########################################################################

# Add as many conditions as you like.
# Please ensure that the folder names are exactly the same
# as in the BioImage Archive.

# To make your life easier, I am copy-pasting the entire list here:
'''
    "Cmin-0-Cmax-0",
    "Cmin-0-Cmax-10nM",
    "Cmin-0-Cmax-50nM",
    "Cmin-0-Cmax-100nM",
    "Cmin-100-Cmax-150nM",
    "Cmin-100-Cmax-200nM",
    "Cmin-0-Cmax-250nM",
    "Cmin-0-Cmax-500nM",
    "Cmin-0-Cmax-1000nM",
    "Cmin-0-Cmax-1500nM",
    "Cmin-0-Cmax-2500nM",
    "Cmin-0-Cmax-5000nM",
    "Cmin-1mM-Cmax-1mM",
    "Cmin-5uM-Cmax-10uM",
    "Cmin-10-Cmax-10nM",
    "Cmin-50-Cmax-50nM",
    "Cmin-10uM-Cmax-10uM",
    "Cmin-10uM-Cmax-20uM",
    "Cmin-25uM-Cmax-50uM",
    "Cmin-0-Cmax-15uM",
    "Cmin-0-Cmax-10uM",
    "Cmin-0-Cmax-25uM",
    "Cmin-0-Cmax-30uM",
    "Cmin-0-Cmax-50uM",
    "Cmin-0-Cmax-100uM",
    "Cmin-0-Cmax-1mM",
    "Cmin-50uM-Cmax-100uM",
    "Cmin-100uM-Cmax-100uM",
    "Cmin-200-Cmax-300nM",
    "Cmin-250-Cmax-500nM",
    "Cmin-500-Cmax-500nM",
    "Cmin-500-Cmax-750nM",
    "Cmin-500-Cmax-1000nM",
    "Cmin-500-Cmax-1500nM",
    "Cmin-1000-Cmax-1500nM",
    "Cmin-1500-Cmax-2500nM",
    "Cmin-1500-Cmax-3000nM",
    "Cmin-2500-Cmax-5000nM",
    "Cmin-5000-Cmax-5000nM",
    "Cmin-5000-Cmax-7500nM"
'''

# Add the required conditions here
CONDITIONS = [
    "Cmin-0-Cmax-0",
]

###########################################################################
# Count JSON files
###########################################################################

def count_jsons(directory):

    if not directory.exists():
        return 0

    return sum(
        1
        for _ in directory.rglob("*.json")
    )


###########################################################################
# Download one condition
###########################################################################

def download_condition(condition):

    #######################################################################
    # Remote JSON directory
    #######################################################################

    remote = (
        f"{REMOTE_ROOT}/"
        f"{condition}/tracks_json/"
    )

    #######################################################################
    # Local condition directory
    #######################################################################

    local_condition = (
        LOCAL_ROOT / condition
    )

    local_condition.mkdir(
        parents=True,
        exist_ok=True
    )

    print()
    print("=" * 75)
    print(f"Condition: {condition}")
    print("=" * 75)

    print(f"Remote:")
    print(f"  {remote}")

    print(f"Local:")
    print(f"  {local_condition}")

    #######################################################################
    # IMPORTANT:
    #
    # The remote path is:
    #
    # ftp.ebi.ac.uk/
    #   pub/
    #   databases/
    #   biostudies/
    #   S-BIAD/
    #   674/
    #   S-BIAD3674/
    #   Files/
    #   ChemoTrack/
    #   condition/
    #   tracks_json/
    #   DATE/
    #   Pos.json
    #
    # We want to remove everything through "tracks_json".
    #
    # There are 10 directories before DATE:
    #
    # 1  pub
    # 2  databases
    # 3  biostudies
    # 4  S-BIAD
    # 5  674
    # 6  S-BIAD3674
    # 7  Files
    # 8  ChemoTrack
    # 9  condition
    # 10 tracks_json
    #
    # Therefore --cut-dirs=10 leaves:
    #
    # DATE/Pos.json
    #######################################################################

    command = [
        "wget",

        "--recursive",

        "--no-parent",

        "--no-host-directories",

        "--cut-dirs=10",

        "--accept=*.json",

        "--continue",

        "--directory-prefix",
        str(local_condition),

        remote
    ]

    print()
    print("Running wget...")
    print()

    print(" ".join(command))
    print()

    result = subprocess.run(
        command
    )

    #######################################################################
    # Count files
    #######################################################################

    json_count = count_jsons(
        local_condition
    )

    #######################################################################
    # Report
    #######################################################################

    if result.returncode == 0:

        print()
        print(
            f"Download completed: "
            f"{json_count:,} JSON files"
        )

    else:

        print()
        print(
            f"wget returned exit code "
            f"{result.returncode}"
        )

        print(
            f"JSON files currently present: "
            f"{json_count:,}"
        )

    return json_count, result.returncode


###########################################################################
# Main
###########################################################################

def main():

    #######################################################################
    # Check wget
    #######################################################################

    try:

        subprocess.run(
            ["wget", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

    except (FileNotFoundError, subprocess.CalledProcessError):

        print(
            "ERROR: wget is not installed."
        )

        return

    #######################################################################
    # Create destination
    #######################################################################

    LOCAL_ROOT.mkdir(
        parents=True,
        exist_ok=True
    )

    #######################################################################
    # Header
    #######################################################################

    print("=" * 75)
    print("ChemoTrack JSON downloader")
    print("=" * 75)

    print(
        f"Conditions: {len(CONDITIONS)}"
    )

    print(
        f"Destination: {LOCAL_ROOT}"
    )

    #######################################################################
    # Download
    #######################################################################

    results = {}

    for i, condition in enumerate(
        CONDITIONS,
        start=1
    ):

        print()
        print(
            f"CONDITION {i}/{len(CONDITIONS)}"
        )

        count, return_code = (
            download_condition(condition)
        )

        results[condition] = (
            count,
            return_code
        )

    #######################################################################
    # Summary
    #######################################################################

    print()
    print()
    print("=" * 75)
    print("DOWNLOAD SUMMARY")
    print("=" * 75)

    total = 0

    for condition in CONDITIONS:

        count, return_code = (
            results[condition]
        )

        total += count

        status = (
            "OK"
            if return_code == 0
            else f"ERROR {return_code}"
        )

        print(
            f"{condition:32s} : "
            f"{count:8,d} JSON files | "
            f"{status}"
        )

    print("-" * 75)

    print(
        f"{'TOTAL':32s} : "
        f"{total:8,d} JSON files"
    )

    print("=" * 75)


###########################################################################
# Run
###########################################################################

if __name__ == "__main__":
    main()
