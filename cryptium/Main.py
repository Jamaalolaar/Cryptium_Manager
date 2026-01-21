from Config_Manager import ConfigManager
from Logger_Manager import LoggerManager
from Command_Line import parse_cli_arguments
import Commands_Map

def extract_overrides(args):
    return {
        key: value
        for key, value in vars(args).items()
        if value is not None and key != "command"
    }

def main():
    
    Config = ConfigManager()
    Logger = LoggerManager(Config)
    args = parse_cli_arguments()
    overrides = extract_overrides(args)
    Config.load_overrides(overrides) #Load CLI overrides into config manager
    

    
    if __name__ == "__main__":
        try:
            
            command_map = {
                "rename": Commands_Map.rename_cmd,
                "sort": Commands_Map.sort_cmd,
                "unsort": Commands_Map.unsort_cmd,
                "find": Commands_Map.find_cmd,
                "delete": Commands_Map.delete_cmd,
                "move": Commands_Map.move_cmd,
                "delete_empty_dirs": Commands_Map.delete_empty_dirs_cmd,
                "create": Commands_Map.create_folder_cmd,
            }

            if args.command in command_map:
                command_map[args.command](args)
            #Cryptium.directory.delete_empty(Cryptium.base_path)
            #Cryptium.rename_file(input("Enter the name of the file to be renamed: "))
            #Cryptium.unfold_files(Cryptium.base_path)

        except Exception as e:
            Logger.log_error(f"Critical error: {e}")
main()