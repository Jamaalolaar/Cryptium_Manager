from .Folder_Sorter_OOP import Directory_Manager, File_Manager, Path
from .Config_Manager import ConfigManager
from .Logger_Manager import LoggerManager
from .Command_Line import parse_cli_arguments
import argparse

Config = ConfigManager()
Logger = LoggerManager(Config)
DM = Directory_Manager(Logger)
Cryptium = File_Manager(Config, Logger, DM)
args = parse_cli_arguments()

class CommandsMap:
    def __init__(self):
        self.commands = {
            "rename": self.rename_cmd,
            "sort": self.sort_cmd,
            "unsort": self.unsort_cmd,
            "find": self.find_cmd,
            "delete": self.delete_cmd,
            "move": self.move_cmd,
            "delete_empty_dirs": self.delete_empty_dirs_cmd,
            "create_folder": self.create_folder_cmd
        }

    def rename_cmd(self, args):
        if args.target:
            target_path = Cryptium.base_path / args.target
        elif args.folder_path:
            target_path = Path(args.folder_path).parent
        else:
            target_path = Cryptium.base_path
        Cryptium.rename_file(args.file_name, target_path)

    def sort_cmd(self, args):
        if args.target:
            target_path = Cryptium.base_path / args.target
        elif args.filepath:
            target_path = Path(args.filepath)
        else:
            target_path = Cryptium.base_path
        Cryptium.fold_file_by_extension(target_path)

    def unsort_cmd(self, args):
        if args.target:
            target_path = Cryptium.base_path / args.target
        elif args.filepath:
            target_path = Path(args.filepath)
        else:
            target_path = Cryptium.base_path
        Cryptium.unfold_files(target_path)

    def find_cmd(self, args):
            Cryptium.find_file(args.file_name, Path(args.target) if args.target else None)
    def delete_cmd(self, args):
        Cryptium.delete_file(args.file_name, Path(args.target) if args.target else None)
    def move_cmd(self, args):
        Cryptium.move_file(args.file_name, args.destination)
    def delete_empty_dirs_cmd(args):    
        if args.target:
            Cryptium.base_path = Cryptium.base_path / args.target
        else: pass  
        Cryptium.directory.delete_empty(Cryptium.base_path)
    def create_folder_cmd(args):
        if args.parent:
            if Path(args.parent).is_dir():
                parent_path = Path(args.parent)
            else:
                parent_path = Cryptium.base_path / args.parent
        else:
            parent_path = Cryptium.base_path
        Cryptium.directory.create_dir(parent_path / args.folder_name)


