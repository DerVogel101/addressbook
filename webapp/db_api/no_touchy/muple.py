import builtins
import sys
from typing import Any, SupportsIndex, Iterator, Union, Iterable


class Muple:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (builtins.tuple, Muple)):
            self.__values = args[0]
        elif len(args) ==1 and isinstance(args[0], Iterable):
            self.__values = builtins.tuple(args[0])
        else:
            self.__values = args

    def __setitem__(self, __key: SupportsIndex, __value: Any) -> None:
        if not isinstance(__key, SupportsIndex):
            raise TypeError(f"tuple indices must be integers or slices, not {type(__key).__name__}")
        new_values = list(self.__values)
        new_values[__key] = __value
        self.__values = builtins.tuple(new_values)

    def __delitem__(self, __key: SupportsIndex) -> None:
        if not isinstance(__key, SupportsIndex):
            raise TypeError(f"tuple indices must be integers or slices, not {type(__key).__name__}")
        new_values = list(self.__values)
        del new_values[__key]
        self.__values = builtins.tuple(new_values)

    def append(self, __object: Any) -> None:
        new_values = list(self.__values)
        new_values.append(__object)
        self.__values = builtins.tuple(new_values)

    def copy(self) -> 'Muple':
        return Muple(self.__values)

    def clear(self) -> None:
        self.__values = builtins.tuple()

    def pop(self, __index: SupportsIndex = -1) -> Any:
        if not isinstance(__index, SupportsIndex):
            raise TypeError(f"pop index must be integer, not {type(__index).__name__}")
        new_values = list(self.__values)
        popped = new_values.pop(__index)
        self.__values = builtins.tuple(new_values)
        return popped

    def extend(self, __iterable: Iterable) -> None:
        if not isinstance(__iterable, Iterable):
            raise TypeError(f"iterable argument required")
        new_values = list(self.__values)
        new_values.extend(__iterable)
        self.__values = builtins.tuple(new_values)

    def insert(self, __index: SupportsIndex, __object: Any) -> None:
        if not isinstance(__index, SupportsIndex):
            raise TypeError(f"insert index must be integer, not {type(__index).__name__}")
        new_values = list(self.__values)
        new_values.insert(__index, __object)
        self.__values = builtins.tuple(new_values)

    def remove(self, __value: Any) -> None:
        new_values = list(self.__values)
        new_values.remove(__value)
        self.__values = builtins.tuple(new_values)
        [1].sort()

    def sort(self, key: None = None, reverse: bool = False) -> None:
        new_values = list(self.__values)
        new_values.sort(key=key, reverse=reverse)
        self.__values = builtins.tuple(new_values)

    # normal tuple methods
    def count(self, __value: Any) -> int:
        return self.__values.count(__value)

    def index(self, __value: Any, __start: SupportsIndex = 0, __stop: SupportsIndex = sys.maxsize) -> int:
        if not isinstance(__start, SupportsIndex) or not isinstance(__stop, SupportsIndex):
            raise TypeError(f"slice indices must be integers or have an __index__ method")
        return self.__values.index(__value, __start, __stop)

    def __repr__(self) -> str:
        return str(self.__values.__repr__())

    def __str__(self) -> str:
        return str(self.__values.__str__())

    def __iter__(self) -> Iterator:
        return self.__values.__iter__()

    def __getitem__(self, __key: SupportsIndex) -> Any:
        if not isinstance(__key, SupportsIndex):
            raise TypeError(f"tuple indices must be integers or slices, not {type(__key).__name__}")
        return self.__values.__getitem__(__key)

    def __len__(self) -> int:
        return len(self.__values)

    def __eq__(self, __value: object) -> bool:
        return self.__values.__eq__(__value)

    def __ne__(self, __value: object) -> bool:
        return self.__values.__ne__(__value)

    def __lt__(self, __value: Union[builtins.tuple, 'Muple']) -> bool:
        if not isinstance(__value, (Muple, builtins.tuple)):
            raise TypeError(f"'<' not supported between instances of 'tuple' and '{type(__value).__name__}'")
        return self.__values.__lt__(builtins.tuple(__value))

    def __le__(self, __value: Union[builtins.tuple, 'Muple']) -> bool:
        if not isinstance(__value, (Muple, builtins.tuple)):
            raise TypeError(f"'<=' not supported between instances of 'tuple' and '{type(__value).__name__}'")
        return self.__values.__le__(builtins.tuple(__value))

    def __gt__(self, __value: Union[builtins.tuple, 'Muple']) -> bool:
        if not isinstance(__value, (Muple, builtins.tuple)):
            raise TypeError(f"'>' not supported between instances of 'tuple' and '{type(__value).__name__}'")
        return self.__values.__gt__(builtins.tuple(__value))

    def __ge__(self, __value: Union[builtins.tuple, 'Muple']) -> bool:
        if not isinstance(__value, (Muple, builtins.tuple)):
            raise TypeError(f"'>=' not supported between instances of 'tuple' and '{type(__value).__name__}'")
        return self.__values.__ge__(builtins.tuple(__value))

    def __hash__(self) -> int:
        return self.__values.__hash__()

    def __add__(self, __value: Union[builtins.tuple, 'Muple']) -> 'Muple':
        if not isinstance(__value, (Muple, builtins.tuple)):
            raise TypeError(f"can only concatenate tuple (not '{type(__value).__name__}') to tuple")
        return Muple(self.__values.__add__(builtins.tuple(__value)))

    def __radd__(self, __value: Union[builtins.tuple, 'Muple']) -> 'Muple':
        if not isinstance(__value, (Muple, builtins.tuple)):
            raise TypeError(f"can only concatenate tuple (not '{type(__value).__name__}') to tuple")
        return Muple(builtins.tuple(__value).__add__(self.__values))

    def __mul__(self, __value: SupportsIndex) -> 'Muple':
        if not isinstance(__value, SupportsIndex):
            raise TypeError(f"can't multiply sequence by non-int of type '{type(__value).__name__}'")
        return Muple(self.__values.__mul__(__value))

    def __rmul__(self, __value: SupportsIndex) -> 'Muple':
        if not isinstance(__value, SupportsIndex):
            raise TypeError(f"can't multiply sequence by non-int of type '{type(__value).__name__}'")
        return Muple(self.__values.__rmul__(__value))

    def __contains__(self, __key: object) -> bool:
        return self.__values.__contains__(__key)

    def __format__(self, __format_spec: str) -> str:
        if not isinstance(__format_spec, str):
            raise TypeError(f"__format__ argument must be str, not {type(__format_spec).__name__}")
        return self.__values.__format__(__format_spec)

    def __reversed__(self):
        return self.__values.__reversed__()


if __name__ == '__main__':
    normal_tuple = (1, 2, 3)
    muple = Muple(1, 2, 3)
    muple[0] = 4
    muple_tuple = Muple(normal_tuple)
    print(muple)
    print(normal_tuple)
    print(muple_tuple)
    print((4, 5, 6) + muple_tuple)
