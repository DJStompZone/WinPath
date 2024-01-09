"""
The `winpath` module provides the `WinPath` class for manipulating and inspecting Windows paths.

The `WinPath` class inherits from `str` and provides additional methods and properties for working
with file paths. It includes methods to get the absolute path, real path, size of the file, stat 
result, join paths, list directory, and properties to get the parent directory, file extension, 
base name. It also includes properties to check if the path is a directory, file, symbolic link, 
mount point, absolute path, or relative path.

Attributes:
    path (str): The normalized path string.
    sep (str): The path separator. Defaults to the os separator.
    pardir (str): The parent directory indicator. Defaults to the os default (usually '..').
    altsep (str): The alternative path separator. Defaults to the os alternative separator.
    extsep (str): The extension separator. Defaults to '.'.

This module relies on the `os` module for interacting with the underlying operating system, and 
the `dataclasses` module for defining the `WinPath` class as a data class.

Example usage:

    from winpath import WinPath

    path = WinPath('C:\\Users\\User\\Documents\\file.txt')
    print(path.abspath())
    print(path.getsize())
    print(path.ext)
"""
import os
from dataclasses import dataclass, field
from typing import Self


@dataclass
class WinPath(str):
    """
    Represents a Windows file path.

    Inherits from `str` and provides additional methods and properties for manipulating and
    inspecting file paths. This class provides methods to get the absolute path, real path,
    size of the file, stat result, join paths, list directory, and properties to get the
    parent directory, file extension, base name, and check if the path is a directory, file,
    symbolic link, mount point, absolute path, or relative path.

    Attributes:
        path (str): The normalized path string.
        sep (str): The path separator. Defaults to the os separator.
        pardir (str): The parent directory indicator. Defaults to the os default (usually '..').
        altsep (str): The alternative path separator. Defaults to the os alternative separator.
        extsep (str): The extension separator. Defaults to '.'.
    """

    path: str
    sep: str = field(default_factory=lambda: os.sep, init=False, repr=False)
    pardir: str = field(default_factory=lambda: os.pardir, init=False, repr=False)
    altsep: str = field(default_factory=lambda: os.altsep, init=False, repr=False)
    extsep: str = field(default_factory=lambda: os.extsep, init=False, repr=False)

    def __post_init__(self) -> None:
        """
        Post-initialization method that normalizes the path and sets the absolute path.

        This method is automatically called after the object is initialized.

        Returns:
            None
        """
        self.__abs_path: str = os.path.normpath(os.path.abspath(self.path))
        self.path = os.path.normpath(self)

    def __truediv__(self, other: Self | str) -> Self:
        """
        Concatenates the current WinPath object with another path or string.

        Args:
            other (WinPath or str): The path or string to be concatenated.

        Returns:
            WinPath: A new WinPath object representing the concatenated path.
        """
        return WinPath(os.path.join(self.path, other))

    def __str__(self) -> str:
        """
        Returns a string representation of the WinPath object.
        """
        return self.path

    def __repr__(self) -> str:
        """
        Returns a printable representation of the WinPath object.
        """
        return f"WinPath({self.path})"

    def exists(self) -> bool:
        """
        Check if the path exists.

        Returns:
            bool: True if the path exists, False otherwise.
        """
        return os.path.exists(self.path)

    def split_path(self: Self) -> tuple[Self, ...]:
        """
        Splits the path into a tuple of WinPath objects.

        Returns:
            tuple[Self, ...]: A tuple of WinPath objects representing the split path.
        """
        segments: tuple[Self, ...] = tuple(
            WinPath(ea) for ea in os.path.split(self.path)
        )
        return segments

    def split_drive(self: Self) -> tuple[Self, ...]:
        """
        Splits the drive from the path.

        Returns:
            tuple[Self, ...]: A tuple containing the drive and the rest of the path.
        """
        segments: tuple[Self, ...] = tuple(
            WinPath(ea) for ea in os.path.splitdrive(self.path)
        )
        return segments

    def split_ext(self: Self) -> tuple[Self, str, str]:
        """
        Splits the extension from the path.

        Returns:
            tuple[Self, str, str]: A tuple where the first element is the path without the
            extension, the second is the base name of the file, and the third is the extension.
        """
        _head, _base = self.split_path()
        return (
            (_head, *os.path.splitext(_base))
            if self.extsep in _base
            else (self, "", "")
        )

    def expand_user(self: Self) -> Self:
        """
        Expands the '~' and '~user' constructs.

        Returns:
            Self: A new WinPath object with the expanded path.
        """
        return WinPath(os.path.expanduser(self.path))

    def expand_vars(self: Self) -> Self:
        """
        Expands the environment variables in the path.

        Returns:
            Self: A new WinPath object with the expanded path.
        """
        return WinPath(os.path.expandvars(self.path))

    def norm_case(self: Self) -> Self:
        """
        Normalizes the case of the path.

        Returns:
            Self: A new WinPath object with the normalized path.
        """
        return WinPath(os.path.normcase(self.path))

    def basename(self: Self) -> Self:
        """
        Returns the base name of the path. This is the second element of the pair returned
        by passing the path to the function split().

        Returns:
            Self: A new WinPath object with the base name of the path.
        """
        return WinPath(os.path.basename(self.path))

    def dirname(self: Self) -> Self:
        """
        Returns the directory name of pathname path. This is the first element of the pair
        returned by passing path to the function split().

        Returns:
            Self: A new WinPath object with the directory name of the path.
        """
        return WinPath(os.path.dirname(self.path))

    def abspath(self: Self) -> Self:
        """
        Returns the absolute version of the path.

        Returns:
            Self: A new WinPath object with the absolute path.
        """
        return WinPath(os.path.abspath(self.path))

    def realpath(self: Self) -> Self:
        """
        Returns the canonical path of the specified filename, eliminating any symbolic links
        encountered in the path.

        Returns:
            Self: A new WinPath object with the real path.
        """
        return WinPath(os.path.realpath(self.path))

    def getsize(self: Self) -> int:
        """
        Returns the size, in bytes, of the path.

        Returns:
            int: The size of the path in bytes.
        """
        return os.path.getsize(self.path)

    def stat(self: Self) -> os.stat_result:
        """
        Performs a stat system call on the given path.

        Returns:
            os.stat_result: The result of the stat call.
        """
        return os.stat(self.path)

    def join_paths(self: Self, *paths: str) -> Self:
        """
        Joins one or more path components intelligently.

        Args:
            *paths (str): An arbitrary number of path components.

        Returns:
            Self: A new WinPath object with the joined path.
        """
        return WinPath(os.path.join(self.path, *paths))

    def listdir(self: Self) -> list[Self]:
        """
        Returns a list containing the names of the entries in the directory given by path.

        Returns:
            list[Self]: A list of WinPath objects representing the entries in the directory.
        """
        return [
            WinPath(self / ea)
            for ea in os.listdir(self.path if self.is_dir else self.parent.path)
        ]

    def ls(self: Self) -> list[Self]:
        """
        A shorthand function for listdir.

        Returns:
            list[Self]: A list of WinPath objects representing the entries in the directory.
        """
        return self.listdir()

    @property
    def parent(self: Self) -> Self:
        """
        Returns the parent directory of the current path.

        Returns:
            Self: A new WinPath object representing the parent directory.
        """
        return WinPath(os.path.dirname(self.__abs_path))

    @property
    def ext(self: Self) -> str:
        """
        Returns the file extension of the current path.

        Returns:
            str: The file extension of the current path.
        """
        return self.split_ext()[-1]

    @property
    def base(self: Self) -> Self:
        """
        Returns the base name of the current path.

        Returns:
            Self: A new WinPath object with the base name of the current path.
        """
        return self.basename()

    @property
    def is_dir(self) -> bool:
        """
        Returns True if the path is a directory.

        Returns:
            bool: True if the path is a directory, False otherwise.
        """
        return os.path.isdir(self.__abs_path)

    @property
    def is_file(self) -> bool:
        """
        Returns True if the path is a regular file.

        Returns:
            bool: True if the path is a regular file, False otherwise.
        """
        return os.path.isfile(self.__abs_path)

    @property
    def is_symlink(self) -> bool:
        """
        Returns True if the path is a symbolic link.

        Returns:
            bool: True if the path is a symbolic link, False otherwise.
        """
        return os.path.islink(self.__abs_path)

    @property
    def is_mount(self) -> bool:
        """
        Returns True if the path is a mount point.

        Returns:
            bool: True if the path is a mount point, False otherwise.
        """
        return os.path.ismount(self.__abs_path)

    @property
    def is_absolute(self) -> bool:
        """
        Returns True if the path is an absolute pathname.

        Returns:
            bool: True if the path is an absolute pathname, False otherwise.
        """
        return os.path.isabs(self.path)

    @property
    def is_relative(self) -> bool:
        """
        Returns True if the path is a relative pathname.

        Returns:
            bool: True if the path is a relative pathname, False otherwise.
        """
        return not os.path.isabs(self.path)
