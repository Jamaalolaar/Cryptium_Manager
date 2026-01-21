from pathlib import Path
import shutil
from .Config_Manager import ConfigManager
from .Logger_Manager import LoggerManager

class Directory_Manager:
    def __init__(self, logger):
        """Initialize"""
        self.logger = logger
    def create_dir(self, path):
        """Creates a directory and logs the action into the info log file. If an
        error is encountered, it logs the error into the error log file."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            self.logger.log_info(f'A new directory {path} was succesfully created!')
        except Exception as e:
            self.logger.log_error(f'Failed to create directory: {path}')
                
                
    def exists(self, path):
        """Returns True if the directory exists, False otherwise"""
        return path.exists() and path.is_dir()
    def scan_all(self, path):
        """Recursively traverse through all files and directories in the given path.
        Yields:
            Path objects for both files and directories found during traversal
        """
        for item in path.iterdir():
            yield item  # First yield the item itself (file or directory)
            if item.is_dir():
                # If it's a directory, recursively scan its contents
                yield from self.scan_all(item)
    def is_empty(self, path):
        """Checks if a directory is empty and returns True if it is, False otherwise"""
        return not any(path.iterdir())
            
    def delete_empty(self, path):
        """Deletes empty directories within the specified path and logs the deletions"""
        for folder in path.rglob("*"):
            if folder.is_dir() and self.is_empty(folder):
                folder.rmdir()
                self.logger.log_info(f'Deleted empty directory: {folder}')
                 

class File_Manager:
    """
    Handles file organization, movement, and extension management within a specified directory
    """
    # Default extensions mapping shared as a class-level constant. Use a copy in __init__ to
    # avoid accidental shared-mutable state between instances.
    EXTENSIONS_DEFAULT = {
        '.txt': 'Text Files',
        '.jpeg': 'Images',
        '.jpg': 'Images',
        '.png': 'Images',
    }
    def __init__(self, config, logger, directory, base_path=None):
        """Initializes File_Manager with config object, logger, and directory manager."""
        self.config = config
        self.base_path = Path.cwd() if base_path is None else Path(base_path)
        extension_dict = self.config.get('extensions')
        
        if extension_dict is None:
            self.extension_dict = dict(self.EXTENSIONS_DEFAULT)
        else:
            self.extension_dict = extension_dict
        self.logger = logger
        self.directory = directory
        
    def move_file(self, src, dest):
        """Moves a single file from src to dst and logs the movement"""
        try:
            shutil.move(str(src), str(dest))
            self.logger.log_info(f'{src.name} was successfully moved to {dest}')
        except (shutil.Error, OSError) as e:
            self.logger.log_error(f'Failed to move {src.name} to {dest}: {e}')
        
    def fold_file_by_extension(self, path=None):
        """
        Move files based on their extensions into categorized folders and logs every movement and error .
        """
        if path is None:
            path = self.base_path
        for file_path in self.directory.scan_all(path):
            if file_path.is_file():
                try:
                    ext = file_path.suffix
                    while ext not in self.extension_dict:
                        response = input(f'Unrecognized extension {ext}! Do you want to assign a folder name to this extension? yes/no: ')
                        if response.lower() == 'yes' or response.lower() == 'y':
                            self.add_new_extension(ext)
                        elif response.lower() == 'no' or response.lower() == 'n':
                            self.add_new_extension(ext, 'Others')
                    
                    folder_name = self.extension_dict.get(ext)
                    new_path = path / folder_name

                    
                    if not self.directory.exists(new_path):
                        self.directory.create_dir(new_path)
                    
                    dest_path = new_path / file_path.name
                    if dest_path.exists():
                        # Handle duplicate file names
                        base_name = file_path.stem
                        suffix = file_path.suffix
                        counter = 1
                        while dest_path.exists():
                            new_name = f"{base_name}_{counter}{suffix}"
                            dest_path = new_path / new_name
                            counter += 1
                    
                    self.move_file(file_path, dest_path)
                    self.logger.log_info(f'File was successfully {file_path.name} moved to {dest_path}') 
                except Exception as e:
                    self.logger.log_error(f"Error processing file {file_path}: {e}")
             
        self.directory.delete_empty(self.base_path)
    def find_file(self, file_name, Path=None):
        """Searches for a file with the given name in the base_path and its subdirectories.
        Returns the Path object if found, otherwise returns None."""
        if Path is None:
            Path = self.base_path
        for file_path in self.directory.scan_all(Path):
            if file_path.is_file() and file_path.stem == file_name:
                print(f'File {file_name} found at {file_path}')
                self.logger.log_info(f'File {file_name} found at {file_path}')
                return file_path
        print(f'File {file_name} not found in {self.base_path} or its subdirectories. Check file name and try again.')
        self.logger.log_info(f'File {file_name} not found in {self.base_path} or its subdirectories.')
        return None

    def add_new_extension(self, ext,Folder_name=None):
        """Adds a new extension and its folder name to the extension dictionary 'extension_dict' and logs it"""
        if Folder_name is None:
            Folder_name = input(f'Enter the folder_name for {ext} files: ')
        self.config.config_data['extensions'][ext] = Folder_name
        self.config.update_config(ext, Folder_name)
        self.extension_dict[ext] = Folder_name
        self.logger.log_info(f'A new extension {ext} was added to the extensions dictionary!')            
        
    def unfold_files(self, path = None):
        """Moves files from subdirectories back to the parent directory and deletes empty folders afterwards"""
        if path is None:
            path = self.base_path
        for file_path in self.directory.scan_all(path):
            if file_path.is_file():
                source = file_path
                destination = path/file_path.name
                self.move_file(source, destination)
            self.directory.delete_empty(path)
        self.directory.delete_empty(path)
        self.logger.log_info(f"{path} was successfully unfolded")    
    
    def rename_file(self, file_name, search_path=None):
        """Renames a file found by `file_name` (stem without suffix).

        Prompts the user for a new name 
        """
        if search_path is None:
            search_path = self.base_path
        old_path = self.find_file(file_name)
        if old_path is None:
            self.logger.log_error(f"Cannot rename: file '{file_name}' not found.")
            return

        try:
            # Ask user for a new name
            user_input = input(f"Enter the new name for the file {old_path.name} ").strip()
            if not user_input:
                self.logger.log_info("Rename cancelled: empty name provided.")
                return

            # Determine the new name and extension
            if Path(user_input).suffix:
                # User provided an extension
                new_name = Path(user_input).name
            else:
                # No extension provided; hence, keep the original extension
                new_name = f"{user_input}{old_path.suffix}"

            # Build the new full path using pathlib
            new_path = old_path.with_name(new_name) #'new_path = old_path.parent / new_name' also works well

            # If target (file name) exists, ask for a new name and restart the process
            candidate = new_path
            if candidate.exists():
                print("A file with that name already exists. Please provide a different name.")
                self.rename_file(file_name)
            else:
                self.move_file(old_path, candidate)
            
        
                

            shutil.move(str(old_path), str(candidate))
            self.logger.log_info(f"Renamed {old_path} -> {candidate}")
        except Exception as e:
            self.logger.log_error(f"Failed to rename {old_path}: {e}")
    
    def delete_file(self, file_name, Path=None):
        """Deletes a specified file and logs the action"""
        file_path = self.find_file(file_name,Path)
        if file_path is None:
            self.logger.log_error(f"Cannot delete: file '{file_name}' not found.")
            return
        elif file_path is not None:
            response = input(f"Are you sure you want to delete the file {file_path.name}? y/n ")
            if response.lower() != 'y':
                self.logger.log_info(f"Deletion of file {file_path.name} cancelled by user.")
                return
            else:
                try:
                    file_path.unlink()
                    self.logger.log_info(f"Deleted file: {file_path}")
                except Exception as e:
                    self.logger.log_error(f"Failed to delete {file_path}: {e}")

        



