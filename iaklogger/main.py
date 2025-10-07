import time
import inspect
from rich.console import Console, Group
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime
from dataclasses import dataclass

DEFAULT = "DEFAULT"  # prints default messages
prepend_tags = []
registered_tags = {}
active_tasks = {}
finished_tasks = {}
CONSOLE = Console()
active_live = None
# live = Live(console=CONSOLE, refresh_per_second=10)
# progress = None
# progress_started = False


@dataclass
class OPTIONS:
    unmuted_tags = []
    """list (Default: Empty): list of allowed tags. Tag DEFAULT is always allowed unless mute_default is true."""
    hidden_tags = []
    """list (Default: Empty): list of hidden tags. Hidden tags will not be printed, but the message will if the tag is in unmuted_tags."""
    log_file = None
    """str (Default: None): File path to save the log. If set, the log will be saved to this file."""
    log_file_max_size_mb = 1024 * 1024 * 10
    """int (Default: 10MB): Maximum size of the log file. If the file exceeds this size, it will be truncated."""
    mute_default = False
    """bool (Default: False): True to mute DEFAULT tag."""
    mute_all = False
    """bool (Default: False): True to mute all logs."""
    newline_after_tag = False
    """bool (Default: False): True to add a newline after tags."""
    show_tags = True
    """bool (Default: False): True to print tags before the message."""
    show_time = False
    """bool (Default: False): True to print time before the message."""


@dataclass
class TaskInfo:
    task_id: int
    task_name: str
    progress: Progress
    # parent_task: Optional[str] = None
    level: int = 0
    completed: bool = False

    # start_order: int = 0  # Track the order tasks were started
    # current_description: str = ""
    # current_progress: float = 0.0
    # current_prefix: str = ""


def check_tags(list1, list2):
    """
    Checks if any tag in list1 is present in list2.

    Args:
        list1 (list): The first list of tags.
        list2 (list): The second list of tags.

    Returns:
        bool: True if all tags from list1 are in list2, False otherwise.
    """
    return all(tag in list2 for tag in list1)


def create_new_task_info(description, task_name, total=100):
    progress = Progress(
        SpinnerColumn(),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("[progress.description]{task.description}"),
    )
    task_id = progress.add_task(description, total)
    task_info = TaskInfo(
        task_id=task_id, task_name=task_name, progress=progress)
    active_tasks[task_name] = task_info
    return task_info


def get_callers_name(FrameInfo):
    if "self" in FrameInfo.frame.f_locals:
        callers_class_name = FrameInfo.frame.f_locals["self"].__class__.__name__
    else:
        callers_class_name = inspect.getmodule(
            FrameInfo.frame).__name__.split(".")[-1]
    return callers_class_name


def get_console():
    # if active_tasks:
    #     last_task_info = list(active_tasks.values())[-1]
    #     return last_task_info.progress.console
    return CONSOLE


def get_prefix(tags, color, new_line=False):
    new_line_str = ""
    tags_str = ""
    time_str = ""
    if OPTIONS.newline_after_tag or new_line:
        new_line_str = "\n"
    if OPTIONS.show_tags:
        tags = [tag.upper() for tag in tags if tag not in OPTIONS.hidden_tags]
        tags_str = f"{'-'.join(tags)} "
    if OPTIONS.show_time:
        time_str = f'{time.strftime("%Y-%m-%d %H:%M:%S")} '
    prefix = f"{time_str}[bold {color}]{tags_str}[/bold {color}]{new_line_str}"
    return prefix


def ignore_warnings():
    mute_tag("WARNING")


def is_printable(tags):
    if not check_tags(tags, OPTIONS.unmuted_tags) and (not check_tags(tags, [DEFAULT]) or OPTIONS.mute_default):
        return False
    elif OPTIONS.mute_all:
        return False
    return True


def log(printable_obj, tags=[], new_line=False, color=None, caller=None):
    """
    Logs the message to the console and/or to a file.
    Args:
        printable_obj (str): Message to log.
        tags (list, optional): List of tags for this message. Default to [DEFAULT].
        new_line (bool, optional): True to add a newline after the tags. Default to False.
    Returns:
        bool: True if the message was logged, False otherwise.
    """
    caller_class_name = get_callers_name(
        inspect.stack()[1]) if caller is None else caller
    if caller_class_name in registered_tags and color is None:
        color = registered_tags[caller_class_name]
    else:
        caller_class_name = DEFAULT

    tags = prepend_tags + [caller_class_name] + tags
    if is_printable(tags):
        console = get_console()
        prefix = get_prefix(tags, color, new_line)
        full_string = f"{prefix}{printable_obj}"
        console.print(full_string)
        if OPTIONS.log_file:
            log_to_file(full_string)
        return True
    return False


def log_error(message):
    """Log errors with special formatting"""
    if "ERROR" not in OPTIONS.unmuted_tags:
        return
    stop_live()
    console = get_console()
    console.print(f"⛔️ [red]ERROR[/red] {message}")
    raise Exception(message)


def log_progress(description, task_name, color=None, caller=None, tags=[], completed=None, last=False):
    global finished_tasks
    global active_tasks

    caller_class_name = get_callers_name(
        inspect.stack()[1]) if caller is None else caller
    if caller_class_name in registered_tags and color is None:
        color = registered_tags[caller_class_name]
    tags = prepend_tags + [caller_class_name] + tags

    if not is_printable(tags):
        return

    prefix = get_prefix(tags, color)
    description = f"{prefix} {description}"

    if not active_tasks:
        global active_live
        active_live = Live(console=CONSOLE, refresh_per_second=10)
        active_live.start()

    if task_name not in active_tasks:
        task_info = create_new_task_info(description, task_name)
    else:
        task_info = active_tasks[task_name]
        if not task_info.progress.finished:
            task_id = task_info.task_id
            progress = task_info.progress
            task = progress.tasks[task_id]
            if completed is None and not last:
                completed = task.completed + 0.3 * (100 - task.completed)
            elif completed is None and last:
                completed = 100
            if completed == 100:
                description = f"[bold green] ✓ {description}"
            progress.update(
                task_id,
                completed=completed,
                description=description,
            )
        if task_info.progress.finished:
            if task_name in finished_tasks:
                finished_tasks[task_name + str(datetime.now())] = task_info
            else:
                finished_tasks[task_name] = task_info
            del active_tasks[task_name]
            if not active_tasks:
                stop_live()

    active_tasks_rendering = reversed(
        [active_tasks[task_name].progress for task_name in active_tasks])
    finished_tasks_rendering = [
        finished_tasks[task_name].progress for task_name in finished_tasks]

    rendered = Group(*finished_tasks_rendering, *active_tasks_rendering)
    active_live.update(rendered)


def stop_live():
    global active_live
    global finished_tasks
    if active_live is not None:
        active_live.stop()
        finished_tasks = {}


def log_to_file(printable_obj):
    """
    Logs the message to a file. The path to the file has to be set in the OPTIONS.log_file attribute.
    Args:
        printable_obj (str): Message to log.
    Returns:
        None
    """
    printable_obj_size = len(printable_obj.encode('utf-8'))
    with open(OPTIONS.log_file, "a+") as f:
        f.seek(0, 2)  # Mueve el puntero al final del archivo
        if f.tell() + printable_obj_size < OPTIONS.log_file_max_size_mb * 1024 * 1024:
            f.write(printable_obj + "\n")
        else:
            f.seek(0)  # Mueve el puntero al principio del archivo
            lines = f.readlines()
            total_size = sum(len(line.encode('utf-8')) for line in lines)
            while lines and total_size + printable_obj_size > OPTIONS.log_file_max_size_mb * 1024 * 1024:
                total_size -= len(lines.pop(0).encode('utf-8'))
            f.seek(0)
            f.truncate()
            f.writelines(lines)
            f.write(printable_obj + "\n")


def log_warning(message):
    """Log warnings with special formatting"""
    if "WARNING" not in OPTIONS.unmuted_tags:
        return
    console = get_console()
    console.print(f"⚠️  [yellow]WARNING[/yellow] {message}")


def mute_tag(tag):
    if tag in OPTIONS.unmuted_tags:
        OPTIONS.unmuted_tags.remove(tag)


def prep_tag(tags: list):
    """
    """
    global prepend_tags
    prepend_tags.append(tags)


def register_self(color, caller=None):
    """
    Register a new tag with a specified color.

    Args:
        obj (object): The class object to be registered.
        color (str): The color for the tag (e.g., "red", "blue", "green").
    """
    class_name = get_callers_name(
        inspect.stack()[1]) if caller is None else caller
    registered_tags[class_name] = color


def restore_warnings():
    unmute_tag("WARNING")


def set_options(opts, verbose=False):
    """
    Set OPTIONS from the provided dictionary opts.

    Parameters:
        opts (dict): A dictionary containing the options to be set.

    Returns:
        None
    """
    if not isinstance(opts, dict):
        raise TypeError("opts must be a dictionary")
    for key, value in opts.items():
        if key not in OPTIONS.__dict__ and verbose:
            log_warning(f"Option {key} not found in OPTIONS")
        setattr(OPTIONS, key, value)


def unmute_tag(tag):
    if tag not in OPTIONS.unmuted_tags:
        OPTIONS.unmuted_tags.append(tag)


def unprep_tag(tags: list):
    """
    """
    global prepend_tags
    prepend_tags = [tag for tag in prepend_tags if tag not in tags]
