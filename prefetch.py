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
    parser.add_argument("-o", "--output", help="Output file to export parsed data")

    ## Prefetch specific arguments
    # these flags do not take values; treat them as boolean switches
    parser.add_argument("--last-run", action="store_true", help="Show the last run time of the application")
    parser.add_argument("--run-count", action="store_true", help="Show the number of times the application has been run")
    parser.add_argument("--open-files", action="store_true", help="List files accessed by the application")

    ## search option to search for a string in the filenames accessed by the different prefetch files
    ## this will only work with the -d option
    parser.add_argument("--search", type=str, help="Search for a string in the filenames accessed by prefetch files in the specified directory")

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
        print("Last Run Time:", pf.get_last_run_time(0))

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

    if args.search:
        if not args.d:
            print("Please provide a directory path with -d to use the --search option.")
            sys.exit(1)
        
        search_term = args.search.lower()
        print(f"Searching for '{search_term}' in prefetch files in directory: {args.d}", end="\n\n")
        for filename in os.listdir(args.d):
            if filename.endswith(".pf"):
                pf = pyscca.open(os.path.join(args.d, filename))
                matched_files = [f for f in pf.filenames if search_term in f.lower()]
                if matched_files:
                    print(f"Executable File: {pf.get_executable_filename()}")
                    for f in matched_files:
                        print(f"  Matched File: {f}")
                    print()

    ### export option 
    ### In csv format we will export the executable name, last run time and run count
    ### In json format we will export all the parsed data
    ### this will only work with the -d option
    ### -o is required to specify the output file
    ### csv format like: executable,last_run,run_count
    ###  in json like { "executable": "name", "last_run": "time", "run_count": count, "files": [list of files] }
    ### two kinds of json jsonl and json array for working with jq command line tool
    if args.export:
        if not args.d:
            print("Please provide a directory path with -d to use the --export option.")
            sys.exit(1)
        if not args.output:
            print("Please provide an output file with -o to export parsed data.")
            sys.exit(1)

        export_data = []
        for filename in os.listdir(args.d):
            if filename.endswith(".pf"):
                pf = pyscca.open(os.path.join(args.d, filename))
                if args.format == "csv":
                    export_data.append(f"{pf.get_executable_filename()},{pf.get_last_run_time(1)},{pf.get_run_count()}")
                elif args.format == "json":
                    files_list = []
                    for f in pf.filenames:
                        files_list.append(str(f))
                    data_entry = {
                        "executable": pf.get_executable_filename(),
                        "last_run": str(pf.get_last_run_time(1)),
                        "run_count": pf.get_run_count(),
                        "files": files_list
                    }
                    export_data.append(data_entry)
                pf.close()

        with open(args.output, "w") as out_file:
            if args.format == "csv":
                out_file.write("executable,last_run,run_count\n")
                for line in export_data:
                    out_file.write(line + "\n")
            elif args.format == "json":
                import json
                json.dump(export_data, out_file, indent=4)

        print(f"Exported parsed data to {args.output} in {args.format} format.")

if __name__ == "__main__":
    main()