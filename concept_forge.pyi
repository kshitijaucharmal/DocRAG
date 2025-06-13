from collections.abc import Iterable, Iterator
from typing import overload


class Vec3:
    def __init__(self, arg0: float, arg1: float, arg2: float, /) -> None:
        """Constructor with x, y, z"""

    @property
    def x(self) -> float: ...

    @x.setter
    def x(self, arg: float, /) -> None: ...

    @property
    def y(self) -> float: ...

    @y.setter
    def y(self, arg: float, /) -> None: ...

    @property
    def z(self) -> float: ...

    @z.setter
    def z(self, arg: float, /) -> None: ...

    def __repr__(self) -> str: ...

class Entity:
    def __init__(self) -> None:
        """Base Class for Entity with transform information"""

    def get_position(self) -> Vec3:
        """Get the Position as a Vec3"""

    def get_rotation(self) -> Vec3:
        """Get the Rotation as a Vec3 (eulerAngles)"""

    def get_scale(self) -> Vec3:
        """Get the Scale as a Vec3"""

    def set_position(self, position: Vec3) -> None:
        """Set the position to a Vec3"""

    def set_rotation(self, rotation: Vec3) -> None:
        """Set the rotation to a Vec3 (eulerAngles)"""

    def set_scale(self, scale: Vec3) -> None:
        """Set the scale to a Vec3"""

    def translate(self, delta: Vec3) -> None:
        """Change the position by Vec3"""

    @overload
    def rotate(self, delta: Vec3) -> None:
        """Change the rotation by Vec3"""

    @overload
    def rotate(self, angle: float, axis: Vec3) -> None:
        """Change the rotation by angle and axis"""

    def scale(self, deltaFactor: Vec3) -> None:
        """Change the scale by Vec3"""

class Cube(Entity):
    def __init__(self, arg: "ShaderManagement::ShaderProgram", /) -> None: ...

class EntityVector:
    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: EntityVector) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: Iterable[Entity], /) -> None:
        """Construct from an iterable object"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the vector is nonempty"""

    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator[Entity]: ...

    @overload
    def __getitem__(self, arg: int, /) -> Entity: ...

    @overload
    def __getitem__(self, arg: slice, /) -> EntityVector: ...

    def clear(self) -> None:
        """Remove all items from list."""

    def append(self, arg: Entity, /) -> None:
        """Append `arg` to the end of the list."""

    def insert(self, arg0: int, arg1: Entity, /) -> None:
        """Insert object `arg1` before index `arg0`."""

    def pop(self, index: int = -1) -> Entity:
        """Remove and return item at `index` (default last)."""

    def extend(self, arg: EntityVector, /) -> None:
        """Extend `self` by appending elements from `arg`."""

    @overload
    def __setitem__(self, arg0: int, arg1: Entity, /) -> None: ...

    @overload
    def __setitem__(self, arg0: slice, arg1: EntityVector, /) -> None: ...

    @overload
    def __delitem__(self, arg: int, /) -> None: ...

    @overload
    def __delitem__(self, arg: slice, /) -> None: ...

    def __eq__(self, arg: object, /) -> bool: ...

    def __ne__(self, arg: object, /) -> bool: ...

    @overload
    def __contains__(self, arg: Entity, /) -> bool: ...

    @overload
    def __contains__(self, arg: object, /) -> bool: ...

    def count(self, arg: Entity, /) -> int:
        """Return number of occurrences of `arg`."""

    def remove(self, arg: Entity, /) -> None:
        """Remove first occurrence of `arg`."""

class ConceptForge:
    def __init__(self) -> None: ...

    def window_should_close(self) -> bool:
        """Check if window should close"""

    def calc_delta_time(self) -> None:
        """Calculate Delta Time"""

    def process_input(self) -> None:
        """Process Input"""

    def render(self) -> None:
        """Clear Screen and Render"""

    def calc_projection(self) -> None:
        """Calculate the Projection Matrix"""

    def gui_management(self) -> None:
        """Draw editor windows"""

    @property
    def window(self) -> "WindowManagement::Window": ...

    @window.setter
    def window(self, arg: "WindowManagement::Window", /) -> None: ...

    @property
    def deltaTime(self) -> float: ...

    @deltaTime.setter
    def deltaTime(self, arg: float, /) -> None: ...

    @property
    def shader_pg(self) -> "ShaderManagement::ShaderProgram": ...

    @shader_pg.setter
    def shader_pg(self, arg: "ShaderManagement::ShaderProgram", /) -> None: ...

    @property
    def input_man(self) -> "InputManagement::Input": ...

    @input_man.setter
    def input_man(self, arg: "InputManagement::Input", /) -> None: ...

    @property
    def entities(self) -> EntityVector: ...

    @entities.setter
    def entities(self, arg: EntityVector, /) -> None: ...

    def set_selected(self, arg: int, /) -> None: ...

    def add_cube(self, position: Vec3, rotation: Vec3, scale: Vec3) -> None:
        """Adds a cube"""
