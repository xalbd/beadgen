import time
from typing import Optional
import math
from build123d import *


def exportSTL(item: Part, name: str, quality: int) -> None:
    """
    Exports a Build123D part as an .stl file.

    Parameters:
    item (Part): the object to export
    name (str): name of the object, used for file naming
    quality (int): quality of the exported .stl, default at 1

    Returns the name of the exported and dumps generated files in the ./generated folder.
    """
    timestr = time.strftime("%y%m%d-%H%M%S")
    stlpath = f"{timestr}-{name}.stl"
    item.export_stl(
        "./generated/" + stlpath, tolerance=0.001 * quality, angular_tolerance=0.1 * quality
    )
    return stlpath


def combineItemList(items: list[Part], offset_amount: float) -> Part:
    """
    Combines a list of Build123D parts into a single object.

    Parameters:
    items (list[Part]): a list of the objects to combine
    offset_amount (float): grid spacing used to lay the objects out

    Returns: Part: objects in items laid out in a grid pattern
    """
    grid_size = math.ceil(math.sqrt(len(items)))
    out = Part()
    for i in range(len(items)):
        out += Pos(i // grid_size * offset_amount, i % grid_size * offset_amount, 0) * items[i]
    return out


def getNonNegFloat(maximum: Optional[float] = None) -> float:
    """
    Allows user input of a non-negative float.

    Parameters:
    maximum (Optional[float]): indicates an exclusive upper bound on the input value; default value is None, which corresponds to an infinite limit

    Returns: float: the first acceptable user input
    """
    dim: float = -1
    print(f"value range: [0, {'inf' if maximum is None else f'{maximum:.2f}'})")

    while True:
        try:
            dim = float(input())
        except ValueError:
            print("not a number, try again")
        else:
            if dim < 0 or (maximum is not None and dim >= maximum):
                print("out of dimension bounds, try again")
            else:
                break
    return dim
