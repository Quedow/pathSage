import os
import sys
import shutil
from pathlib import Path

class pathSage():
    def as_path(self, path: str | Path) -> str:
        """This function allows to normalize the path put as parameter and return it as a string to be readable by all functions that need a path. It checks if the parameter is a string or a Path. It also checks if the path exists else it generate a ValueError: PEBCAK.

        Args:
            path (str | Path): the path that needs to be normalized.

        Returns:
            str: the input path normalized.
        """
        
        if not self.exists(path): return self.error_e()
        return Path(path).as_posix() + '/'
    
    def as_file(self, path: str | Path) -> str:
        """This function allows to normalize the file path put as parameter and return it as a string to be readable by all functions that need a path. It checks if the parameter is a string or a Path. It also checks if the file exists else it generate a ValueError: PEBCAK.

        Args:
            file path (str | Path): the file path that needs to be normalized.

        Returns:
            str: the input file path normalized.
        """

        if not self.exists(path): return self.error_e()
        return Path(path).as_posix()
    
    def as_new_path(self, path: str | Path) -> str:
        """This function allows to normalize the path put as parameter and return it as a string to be readable by all functions that need a path. It checks if the parameter is a string or a Path. As it's a new path, it doesn't yet exist, so the function doesn't check the path's existence.

        Args:
            path (str | Path): the path that needs to be normalized.

        Returns:
            str: the input path normalized.
        """

        if not self.valid(path): return self.error_f()
        return Path(path).as_posix() + '/'
    
    def as_new_file(self, path: str | Path) -> str:
        """This function allows to normalize the file path put as parameter and return it as a string to be readable by all functions that need a path. It checks if the parameter is a string or a Path. As it's a new file path, it doesn't yet exist, so the function doesn't check the file path's existence.

        Args:
            file path (str | Path): the file path that needs to be normalized.

        Returns:
            str: the input file path normalized.
        """

        if not self.valid(path): return self.error_f()
        return Path(path).as_posix()
    
    def as_extension(self, extension: str) -> str:
        """This function normalizes the extension set as a parameter, adding a dot at the beginning if it hasn't already been done.

        Args:
            extension (str): the file extension.

        Returns:
            str: the file extension normalized.
        """

        return (
            f".{extension}"
            if not extension.startswith('.')
            else extension
        )
    
    def as_cmd(self, path: str | Path) -> str:
        """This function converts the path set as parameter to be understood by Windows cmd or shell. It checks if the parameter is a string or a Path. It also checks if the path exists else it generate a ValueError: PEBCAK.

        Args:
            path (str | Path): the path that needs to be converted.

        Returns:
            str: the input path converted (containing backslashes instead of slashes).
        """

        return os.path.realpath(self.as_path(path))
    
    def for_win(self, path: str) -> str:
        """This function converts the path or file path as Windows path (with backslashes). It checks if the parameter is a string else it generate a ValueError: PEBCAK.

        Args:
            path (str | Path): the path or file path that needs to be converted.

        Returns:
            str: the input path converted (containing backslashes instead of slashes).
        """

        if not isinstance(path, str): return self.error_f()
        return path.replace('/', '\\')
    
    def join(self, root: str | Path, elements: list[str]) -> Path:
        """This function allows to use joinpath from pathlib with Path but also with string parameters.

        Args:
            root (str | Path): the path to a specific directory.
            elements (list): the list of sub directories and/or file of the root path.

        Returns:
            Path: the concatenate path. You can use 'as_path()' or 'as_new_path()' to normalize it as string.
        """

        if not self.valid(root): return self.error_f()

        path = Path(root)
        for element in elements:
            path = path.joinpath(element)
        return path
    
    def stem(self, path: str | Path) -> str:
        """This function allows to get file name from file path (without extension).

        Args:
            path (str | Path): the file path containing the file name to extract.

        Returns:
            str: the file name without extension.
        """

        if not self.valid(path): return self.error_f()
        return Path(path).stem

    def name(self, path: str | Path) -> str:
        """This function allows to get file name from file path (with extension).

        Args:
            path (str | Path): the file path containing the file name to extract.

        Returns:
            str: the file name with extension.
        """

        if not self.valid(path): return self.error_f()
        return Path(path).name
    
    def suffix(self, path: str | Path) -> str:
        """This function allows to get file extension from file path.

        Args:
            path (str | Path): the file path containing the extension to extract.

        Returns:
            str: the file extension.
        """

        if not self.valid(path): return self.error_f()
        return Path(path).suffix
    
    def parent_path(self, path: str | Path, parent_nb: int) -> str:
        """This function allows to get the n-th parent path from the path defined as parameter.

        Args:
            path (str | Path): the child path as start point.
            parent_nb (int): the n-th parent needed.

        Returns:
            str: the n-th parent path normalized.
        """
        
        parent_path = Path(path)
        for _ in range(parent_nb):
            parent_path = parent_path.parent
        return self.as_path(parent_path)
    
    def get_location(self, file_path: str | Path) -> str:
        """This function allows to get the current file location even if it a python script or an executable file.

        Args:
            file_path (str | Path): the file path to get its location.

        Returns:
            str: the current location of the file passed as parameter.
        """

        if getattr(sys, 'frozen', False):
            return self.as_path(os.path.dirname(sys.executable))
        else:
            return self.as_path(self.parent_path(file_path, 1))
    
    def exists(self, path: str | Path) -> bool:
        """This function checks whether the path or file defined as a parameter have a correct type (Path or str) and exists.

        Args:
            path (str | Path): the path or file to check.

        Returns:
            bool: true if path or file exists else false.
        """

        if self.valid(path):
            return Path(path).exists()
        else:
            return False
        
    def valid(self, path: str | Path) -> bool:
        """This function checks whether the path or file defined as a parameter have a correct type (Path or str).

        Args:
            path (str | Path): the path or file to check.

        Returns:
            bool: true if path or file type is correct else false.
        """

        return isinstance(path, Path) or isinstance(path, str)
    
    def has_extension(self, path: str | Path, extension: str) -> bool:
        """This function compares a file path with an extension defined as parameters (case insensitive).

        Args:
            path (str | Path): the file path to check.
            extension (str): the reference extension.

        Returns:
            bool: true if the file has the same extension as the reference extension else false.
        """
        
        if not self.exists(path): return self.error_e()
        
        if isinstance(extension, str):
            extension = [extension]

        return (Path(path).suffix.lower() in [e.lower() for e in extension]) and Path(path).is_file()
    
    def file_start(self, path: str | Path, pattern: str) -> bool:
        """This function checks if the file name, containing in a path, starts with a defined pattern.

        Args:
            path (str | Path): the path containing the file name.
            pattern (str): the pattern to compare with the file name.

        Returns:
            bool: true if the file name starts with the pattern else false.
        """

        return self.stem(path).startswith(pattern)
    
    def file_end(self, path: str | Path, pattern: str) -> bool:
        """This function checks if the file name, containing in a path, ends with a defined pattern.

        Args:
            path (str | Path): the path containing the file name.
            pattern (str): the pattern to compare with the file name.

        Returns:
            bool: true if the file name ends with the pattern else false.
        """

        return self.self.stem(path).endswith(pattern)
    
    def similar_file(self, path: str | Path, start: str='', end: str='') -> str:
        """This function allows to get an existing file path similar to the file path defined as parameter by editing the start and the end of the file name.

        Args:
            path (str | Path): the file path.
            start (str, optional): the pattern at the beginning of the peer file name. Defaults to ''.
            end (str, optional): the pattern at the end of the peer file name. Defaults to ''.

        Returns:
            str: the peer file path normalized of the input file path.
        """

        file = start + self.name(path) + end
        return self.as_file(self.join(Path(path).parent, [file]))

    def get_files_path(self, path: str | Path, pattern: str=None, extension: str=None) -> list[str]:
        """This function allows to get all file paths from the path defined as parameter. It can also filter results by using pattern or extension extraction.

        Args:
            path (str | Path): the path that contains files to extract.
            pattern (str, optional): the pattern contained in file names to extract. Defaults to None.
            extension (str, optional): the extension of files to extract. Defaults to None.

        Returns:
            list: the list of file paths normalized.
        """

        if pattern is not None and extension is not None:
            return [self.as_file(file) for file in Path(path).iterdir() if pattern in file.stem and self.has_extension(file, extension)]
        elif pattern is not None:
            return [self.as_file(file) for file in Path(path).iterdir() if pattern in file.stem]
        elif extension is not None:
            return [self.as_file(file) for file in Path(path).iterdir() if self.has_extension(file, extension)]
        else:
            return [self.as_file(file) for file in Path(path).iterdir()]
    
    def get_files_stem(self, path: str | Path, pattern: str=None, extension: str=None) -> list[str]:
        """This function allows to get all file names (without extension) from the path defined as parameter. It can also filter results by using pattern or extension extraction.

        Args:
            path (str | Path): the path that contains files to extract.
            pattern (str, optional): the pattern contained in file names to extract. Defaults to None.
            extension (str, optional): the extension of files to extract. Defaults to None.

        Returns:
            list: the list of file names (without extension).
        """

        if pattern is not None and extension is not None:
            return [file.stem for file in Path(path).iterdir() if pattern in file.stem and self.has_extension(file, extension)]
        elif pattern is not None:
            return [file.stem for file in Path(path).iterdir() if pattern in file.stem]
        elif extension is not None:
            return [file.stem for file in Path(path).iterdir() if self.has_extension(file, extension)]
        else:
            return [file.stem for file in Path(path).iterdir()]
        
    def get_files_name(self, path: str | Path, pattern: str=None, extension: str=None) -> list[str]:
        """This function allows to get all file names (with extension) from the path defined as parameter. It can also filter results by using pattern or extension extraction.

        Args:
            path (str | Path): the path that contains files to extract.
            pattern (str, optional): the pattern contained in file names to extract. Defaults to None.
            extension (str, optional): the extension of files to extract. Defaults to None.

        Returns:
            list: the list of file names (with extension).
        """

        if pattern is not None and extension is not None:
            return [file.name for file in Path(path).iterdir() if pattern in file.stem and self.has_extension(path, extension)]
        elif pattern is not None:
            return [file.name for file in Path(path).iterdir() if pattern in file.stem]
        elif extension is not None:
            return [file.name for file in Path(path).iterdir() if self.has_extension(path, extension)]
        else:
            return [file.name for file in Path(path).iterdir()]
        
    def mkdir(self, folder_path: str | Path) -> str:
        """This function just creation a simple folder and check before if the folder doesn't already exist.

        Args:
            folder_path (str | Path): the folder path to create.

        Returns:
            str: the folder path created.
        """
        
        if not self.exists(folder_path):
            os.mkdir(folder_path)
        return self.as_file(folder_path)
    
    def move(self, current_path: str | Path, destination_path: str | Path, is_path: bool=True) -> None:
        """This function allows to move a file or a folder in a new location.

        Args:
            current_path (str | Path): the file or folder path to move.
            destination_path (str | Path): the destination path.
            is_path (bool, optional): True if current_path a folder path else False. Defaults to True.
        """

        destination_path = self.mkdir(destination_path)

        if is_path:
            current_path = self.as_path(current_path)
        else:
            current_path = self.as_file(current_path)

        shutil.move(current_path, destination_path)

    def copy(self, file_path : str | Path, destination_path: str | Path, new_file_name: None | str=None) -> None:
        """This function allow to copy a file and past it in new location. There is also the possibility to rename it in its new location.

        Args:
            file_path (str | Path): the file path to copy.
            destination_path (str | Path): the destination path where to past the file.
            new_file_name (None | str, optional): the new file name of pasted file. Defaults to None.
        """

        file_path = self.as_file(file_path)
        destination_path = self.as_path(destination_path)

        if not self.exists(self.join(destination_path, [new_file_name or self.name(file_path)])):
            new_file_path = shutil.copy2(file_path, destination_path)

            if new_file_name is not None:
                self.rename(new_file_path, self.as_new_file(self.join(destination_path, [new_file_name])))
        
    def delete(self, file_path: str | Path) -> None:
        """This function allows to delete a file. It also checks if the parameter is a string or a Path and if the file exists else it generate a ValueError: PEBCAK.

        Args:
            file_path (str | Path): the file path to delete.
        """

        os.remove(self.as_file(file_path))

    def rename(self, current_path: str | Path, new_path: str | Path) -> None:
        """This function allows to rename a directory or file name.

        Args:
            current_path (str | Path): the file or directory path that need to be renamed.
            new_path (str | Path): the new file or directory path.
        """

        if not self.exists(current_path): return self.error_e()
        if not self.valid(new_path): return self.error_f()

        Path(current_path).rename(new_path)
    
    def error_f(self):
        raise ValueError("PEBCAK : Problem Exists Between Chair And Keyboard. Wrong parameter type.")
    
    def error_e(self):
        raise ValueError("PEBCAK : Problem Exists Between Chair And Keyboard. The path or file defined in the parameter does not exist (or its type is incorrect).")