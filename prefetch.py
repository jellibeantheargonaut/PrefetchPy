## A python tool to parse windows prefetch files
## uses libscca-python library

import os
import sys
import argparse

import pyscca

BANNER = r"""
▗▄▄▖ ▗▄▄▖ ▗▄▄▄▖▗▄▄▄▖▗▄▄▄▖▗▄▄▄▖▗▄▄▖▗▖ ▗▖
▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌   ▐▌     █ ▐▌   ▐▌ ▐▌
▐▛▀▘ ▐▛▀▚▖▐▛▀▀▘▐▛▀▀▘▐▛▀▀▘  █ ▐▌   ▐▛▀▜▌
▐▌   ▐▌ ▐▌▐▙▄▄▖▐▌   ▐▙▄▄▖  █ ▝▚▄▄▖▐▌ ▐▌
                                                                               
=========================================================

Prefetch:   A python tool to parse windows prefetch files
Author:     @jellibeantheargonaut

=========================================================
"""

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Prefetch: Parse Windows Prefetch files")

    ## basic arguments and options
    # make the file argument positional so it must be the first argument
    parser.add_argument("-f","--file", help="Path to the prefetch file to parse")
    parser.add_argument("-d", help="Path to the directory containing prefetch files")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-o", "--output", help="Output file to save the parsed data")

    ## Prefetch specific arguments
    # these flags do not take values; treat them as boolean switches
    parser.add_argument("--last-run", action="store_true", help="Show the last run time of the application")
    parser.add_argument("--run-count", action="store_true", help="Show the number of times the application has been run")
    parser.add_argument("--open-files", action="store_true", help="List files accessed by the application")

    ## directory specific arguments
    parser.add_argument("--timeline", action="store_true", help="List the timeline of executions")
    parser.add_argument("--export", action="store_true", help="Export parsed data to a file")

    ## format argument takes options csv, json

    parser.add_argument("--format", choices=["json", "csv"], default="json",
                        help="Specify the export format when exporting parsed data (json or csv). Defaults to json.")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    ## Get last run time
    if args.last_run:
        pf = pyscca.open(args.file)
        print("Last Run Time:", pf.get_last_run_time(-1))

    if args.run_count:
        pf = pyscca.open(args.file)
        print("Run Count:", pf.get_run_count())

    if args.open_files:
        pf = pyscca.open(args.file)
        print("Open Files:")
        for f in pf.filenames:
            print(f)

    if args.timeline:
        if not args.d:
            print("Please provide a directory path with -d to use the --timeline option.")
            sys.exit(1)
        
        ### print the applications run count and sort them by last run time
        timeline = []
        for filename in os.listdir(args.d):
            if filename.endswith(".pf"):
                pf = pyscca.open(os.path.join(args.d, filename))
                timeline.append((pf.get_executable_filename(), pf.get_last_run_time(1), pf.get_run_count()))
        # sort by last run time
        timeline.sort(key=lambda x: x[1], reverse=True)
        print("Timeline of Executions:",end="\n\n")
        for entry in timeline:

            ## this is a bit clunky but formats the last run time nicely
            formatted_time = entry[1].strftime("%Y-%m-%d %H:%M:%S") if entry[1] else "N/A"

            ## print all the details in equitable spacing
            print(f"File: {entry[0]:<30} Last Run: {formatted_time:<20} Run Count: {entry[2]:<5}")

if __name__ == "__main__":
    main()