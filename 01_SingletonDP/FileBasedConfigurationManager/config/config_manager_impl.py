from __future__ import annotations
from typing import Type, Any

from .config_manager import FileBasedConfigurationManager


class FileBasedConfigurationManagerImpl(FileBasedConfigurationManager):

    _instance = None
    @staticmethod
    def get_instance() -> FileBasedConfigurationManager:
        if FileBasedConfigurationManagerImpl._instance is None:
            FileBasedConfigurationManagerImpl._instance = (
                FileBasedConfigurationManagerImpl()         
            )
        return FileBasedConfigurationManagerImpl._instance

    @staticmethod
    def reset_instance() -> None:
        FileBasedConfigurationManagerImpl._instance = None

    def get_configuration(self, key: str) -> str:
        return self.properties.get(key)

    def get_configuration_with_type(self, key: str, type_: Type) -> Any:
        value = self.get_configuration(key)
        if value is None:
            return None
        
        return self.convert(value, type_)
    
    def set_configuration(self, key: str, value: str) -> None:
        self.properties[key] = value

    def remove_configuration(self, key: str) -> None:
        self.properties.pop(key, None)

    def clear(self) -> None:
        self.properties.clear()


"""
here we are creating the object and assigning to the _instance valirable

FileBasedConfigurationManagerImpl._instance = (
                FileBasedConfigurationManagerImpl()  

FileBasedConfigurationManagerImpl()
            |
            v
        __new__()
            |
            v
        __init__()
            |
            v
      Return Object
"""

"""
Let's Understand Each Method
1. _instance
_instance = None

Class variable.

Shared by all calls to:

FileBasedConfigurationManagerImpl.get_instance()

Initial state:

_instance -> None
2. get_instance()
if FileBasedConfigurationManagerImpl._instance is None:

First call:

_instance = None

Condition is True.

Creates:

FileBasedConfigurationManagerImpl()

Stores it:

_instance = object

Returns it.

Second call:

_instance != None

Condition becomes False.

Returns existing object.

Example:

obj1 = FileBasedConfigurationManagerImpl.get_instance()
obj2 = FileBasedConfigurationManagerImpl.get_instance()

print(obj1 is obj2)

Output:

True
3. reset_instance()
FileBasedConfigurationManagerImpl._instance = None

Resets Singleton.

Example:

obj1 = get_instance()

reset_instance()

obj2 = get_instance()

Now:

obj1 is obj2

returns:

False

because a new object was created.

4. get_configuration()
return self.properties.get(key)

Example:

{
    "PORT": "5432"
}

Call:

get_configuration("PORT")

Returns:

"5432"

Missing key:

get_configuration("ABC")

Returns:

None
5. get_configuration_with_type()

Instead of duplicating lookup logic:

value = self.get_configuration(key)

Reuse existing method.

Example:

{
    "PORT": "5432"
}

Call:

get_configuration_with_type(
    "PORT",
    int
)

Flow:

value = "5432"

convert("5432", int)

return 5432

Conversion failure:

{
    "PORT": "ABC"
}

Call:

get_configuration_with_type(
    "PORT",
    int
)

Inside:

int("ABC")

Raises:

ValueError

which is exactly what the base class intends.

6. set_configuration()
self.properties[key] = value

Example:

set_configuration(
    "PORT",
    "5432"
)

Result:

{
    "PORT": "5432"
}

Overwrite:

set_configuration(
    "PORT",
    "9999"
)

Result:

{
    "PORT": "9999"
}
7. remove_configuration()
self.properties.pop(key, None)

Why not:

del self.properties[key]

Because:

del

raises:

KeyError

for missing keys.

Using:

pop(key, None)

makes removal idempotent.

remove_configuration("PORT")
remove_configuration("PORT")
remove_configuration("PORT")

No errors.

8. clear()
self.properties.clear()

Before:

{
    "PORT": "5432",
    "HOST": "localhost"
}

After:

{}

Important:

Singleton object still exists.

Only the dictionary is emptied.

Interview Takeaway

If an interviewer asks:

Why Singleton here?

A strong answer is:

The configuration manager represents a shared application-wide state. Multiple instances could maintain different copies of configuration data, leading to inconsistent behavior. Singleton ensures a single source of truth for configuration across the application.

That's much stronger than:

Because the assignment said to use Singleton.
"""