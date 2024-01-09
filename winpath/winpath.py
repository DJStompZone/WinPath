import os
from typing import Self

from dataclasses import dataclass, field

@dataclass
class WinPath(str):
    path: str
    sep: str = field(default_factory=lambda: os.sep, init=False, repr=False)
    pardir: str = field(default_factory=lambda: os.pardir, init=False, repr=False)
    altsep: str = field(default_factory=lambda: os.altsep, init=False, repr=False)
    extsep: str = field(default_factory=lambda: os.extsep, init=False, repr=False)
    
    def __post_init__(self) -> None:
        self.__abs_path: str = os.path.normpath(os.path.abspath(self.path))
        self.path = os.path.normpath(self)
    
    def __truediv__(self, other: Self | str) -> Self:
        return WinPath(os.path.join(self.path, other))
    
    def __str__(self) -> str:
        return self.path
    
    def __repr__(self) -> str:
        return f"WinPath({self.path})"
    
    def exists(self) -> bool:
        return os.path.exists(self.path)
    
    def split_path(self: Self) -> tuple[Self, ...]:
        segments: tuple[Self, ...] = tuple(
            WinPath(ea) for ea in os.path.split(self.path)
        )
        return segments
    
    def split_drive(self: Self) -> tuple[Self, ...]:
        segments: tuple[Self, ...] = tuple(
            WinPath(ea) for ea in os.path.splitdrive(self.path)
        )
        return segments
    
    def split_ext(self: Self) -> tuple[Self, str, str]:
        _head, _base = self.split_path()
        return (
            (_head, *os.path.splitext(_base))
            if self.extsep in _base
            else (self, "", "")
        )
    
    def expand_user(self: Self) -> Self:
        return WinPath(os.path.expanduser(self.path))
    
    def expand_vars(self: Self) -> Self:
        return WinPath(os.path.expandvars(self.path))
    
    def norm_case(self: Self) -> Self:
        return WinPath(os.path.normcase(self.path))
    
    def basename(self: Self) -> Self:
        return WinPath(os.path.basename(self.path))
    
    def dirname(self: Self) -> Self:
        return WinPath(os.path.dirname(self.path))
    
    def abspath(self: Self) -> Self:
        return WinPath(os.path.abspath(self.path))
    
    def realpath(self: Self) -> Self:
        return WinPath(os.path.realpath(self.path))
    
    def getsize(self: Self) -> int:
        return os.path.getsize(self.path)
    
    def stat(self: Self) -> os.stat_result:
        return os.stat(self.path)
    
    def join_paths(self: Self, *paths: str) -> Self:
        return WinPath(os.path.join(self.path, *paths))
    
    def listdir(self: Self) -> list[Self]:
        return [
            WinPath(self / ea)
            for ea in os.listdir(self.path if self.is_dir else self.parent.path)
        ]
    
    def ls(self: Self) -> list[Self]:
        return self.listdir()
    
    @property
    def parent(self: Self) -> Self:
        return WinPath(os.path.dirname(self.__abs_path))
    
    @property
    def ext(self: Self) -> str:
        return self.split_ext()[-1]
    
    @property
    def base(self: Self) -> Self:
        return self.basename()
    
    @property
    def is_dir(self) -> bool:
        return os.path.isdir(self.__abs_path)
    
    @property
    def is_file(self) -> bool:
        return os.path.isfile(self.__abs_path)
    
    @property
    def is_symlink(self) -> bool:
        return os.path.islink(self.__abs_path)
    
    @property
    def is_mount(self) -> bool:
        return os.path.ismount(self.__abs_path)
    
    @property
    def is_absolute(self) -> bool:
        return os.path.isabs(self.path)
    
    @property
    def is_relative(self) -> bool:
        return not os.path.isabs(self.path)

