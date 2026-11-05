"""
Script to print all the available environments in the extension.

The script iterates over all registered environments and stores the details in a table.
It prints the name of the environment, the entry point and the config file.
"""

import gymnasium as gym
from prettytable import PrettyTable

# Import extensions to set up environment tasks
import basic_locomotion_isaaclab.tasks  # noqa: F401


def main():
    """Print all environments registered in `isaac.lab_demo` extension."""
    # print all the available environments
    table = PrettyTable(["S. No.", "Task Name", "Entry Point", "Config"])
    table.title = "Available Environments in Isaac Lab Template Extension"
    # set alignment of table columns
    table.align["Task Name"] = "l"
    table.align["Entry Point"] = "l"
    table.align["Config"] = "l"

    # count of environments
    index = 0
    # acquire all Isaac environments names
    for task_spec in gym.registry.values():
        if "Template-" in task_spec.id:
            # add details to table
            table.add_row([index + 1, task_spec.id, task_spec.entry_point, task_spec.kwargs["env_cfg_entry_point"]])
            # increment count
            index += 1

    print(table)


if __name__ == "__main__":
    # registering the tasks needs no simulation runtime, so nothing is launched here
    main()
