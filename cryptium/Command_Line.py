import argparse
from pathlib import Path
def parse_cli_arguments():
    parser = argparse.ArgumentParser(prog="Cryptium Manager",description="Cryptium Manager, a tool to manage files and folders.")
    parser.add_argument("--v","--version", action="version", version="Cryptium Manager 1.0.0")
    subparsers = parser.add_subparsers(dest="command", required="True")
    sort_parser = subparsers.add_parser("sort")
    sort_parser.add_argument("--dry-run", action="store_true", help="Simulate the actions without making any changes.")
    sort_parser.add_argument("--target", type=str, help="Directory to be sorted.")
    sort_parser.add_argument("--folderpath", type=str, help="Path of the directory (if target directory is outside the current directory).")
    
    unsort_parser = subparsers.add_parser("unsort")
    unsort_parser.add_argument("--dry-run", action="store_true", help="Simulate the actions without making any changes.")
    unsort_parser.add_argument("--target", type=str, help="Directory to be unsorted.")
    unsort_parser.add_argument("--folderpath", type=str, help="Path of the directory (if target directory is outside the current directory).")
    
    rename_parser = subparsers.add_parser("rename")
    rename_parser.add_argument("--file_name", type=str, help="Name of the file to be renamed (without extension).")
    rename_parser.add_argument("--target", type=str, help="Directory where the file is located.")
    rename_parser.add_argument("--folder_path", type=str, help="Full path of the file to be renamed.")

    find_parser = subparsers.add_parser("find")
    find_parser.add_argument("--file_name", type=str, help="Name of the file to be found (without extension).")
    find_parser.add_argument("--folder", type=str, help= "Directory to search in.")

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("file_name", type=str, help="Name of the file to be deleted (without extension).")
    delete_parser.add_argument("--folder", type=str, help= "Directory to search in.")

    move_parser = subparsers.add_parser("move")
    move_parser.add_argument("file_name", type=str, help="Name of the file to be moved (without extension).")
    move_parser.add_argument("--destination", type=str, help="Destination directory.")

    delete_empty_parser = subparsers.add_parser("delete_empty_dirs")
    delete_empty_parser.add_argument("--target", type=str, help="Directory to delete empty folders from.")

    create_folder_parser = subparsers.add_parser("create")
    create_folder_parser.add_argument("folder_name", type=str, help="Name of the folder to be created.")
    create_folder_parser.add_argument("--parent", type=str, help="Parent directory where the folder will be created.")

    config_parser = subparsers.add_parser("config")
    config_parser.add_argument("custom_mapping", type=str, help="Path to custom config file.")
    config_parser.add_argument("--dry-run", action="store_true", help="Simulate the actions without making any changes.")
    config_parser.add_argument("--set-defaults", action="store_true", help="Reset to default settings.")

    



    #metavar
    return parser.parse_args()