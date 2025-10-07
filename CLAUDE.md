# iaklogger - Project Guide for Claude Code

## Project Overview

**iaklogger** is a simple, tag-based logging library for Python. It provides an easy-to-use interface for logging messages with customizable filtering, file output, and rich console formatting.

## Project Structure

```
iaklogger/
├── iaklogger/
│   ├── __init__.py          # Package initialization, exports main API
│   ├── iaklogger.py         # Core implementation
│   └── test_iaklogger.py    # Tests
├── setup.py                 # Package distribution configuration
├── setup.cfg                # Additional setup configuration
├── README.md                # User-facing documentation with examples
├── licence.txt              # MIT License
└── MANIFEST                 # Package manifest
```

## Core Concepts

### Tags
- Messages are associated with one or more tags
- Tags control which messages are printed
- The `DEFAULT` tag is always applied to messages without explicit tags
- Tags can be used to organize logs by module, feature, or severity

### OPTIONS Configuration
The `OPTIONS` dataclass controls logging behavior:
- `unmuted_tags`: List of tags that are allowed to print (default: empty, prints all)
- `hidden_tags`: Tags that won't be displayed but messages still print if tag is unmuted
- `log_file`: File path for saving logs (default: None)
- `log_file_max_size_mb`: Maximum log file size before truncation (default: 10MB)
- `mute_default`: Suppress DEFAULT tag messages (default: False)
- `mute_all`: Suppress all logs (default: False)
- `newline_after_tag`: Add newline after tag prefix (default: False)
- `show_tags`: Display tags in output (default: True)
- `show_time`: Display timestamp in output (default: False)

## Main API

### Basic Functions
- `log(message, tags=[], new_line=False, color=None, caller=None)`: Log a message
- `set_options(opts, verbose=False)`: Set multiple options from a dictionary
- `unmute_tag(tag)`: Allow a tag to print
- `mute_tag(tag)`: Block a tag from printing

### Advanced Functions
- `register_self(color, caller=None)`: Register a class/module with a color
- `log_progress(description, task_name, color=None, caller=None, tags=[], completed=None, last=False)`: Progress tracking with rich UI
- `log_warning(message)`: Log warnings with special formatting
- `log_error(message)`: Log errors and raise exception
- `prep_tag(tags)`: Prepend tags to all subsequent logs
- `unprep_tag(tags)`: Remove prepended tags

## Dependencies

- **rich**: For console formatting, progress bars, and styled output
- **Python standard library**: time, inspect, datetime, dataclasses

## Development Notes

### Key Implementation Details

1. **Tag Filtering**: `check_tags()` verifies all tags in a message are in the unmuted list
2. **Caller Detection**: `get_callers_name()` uses inspect to automatically detect the calling class/module
3. **File Logging**: Circular buffer implementation prevents unbounded file growth
4. **Rich Integration**: Uses Rich library's Console, Progress, and Live for interactive terminal output

### Version History
- Current version: 1.0.7
- Development stage: Alpha
- Repository: https://github.com/Iakl/iaklogger

### Testing
- Tests located in `iaklogger/test_iaklogger.py`
- Run tests with: `python -m pytest iaklogger/test_iaklogger.py`

## Common Tasks

### Making Changes
1. **Modify core logic**: Edit `iaklogger/iaklogger.py`
2. **Update API**: Modify both `iaklogger.py` and `__init__.py` exports
3. **Update version**: Change version in `setup.py`
4. **Update docs**: Modify `README.md` with usage examples

### Building and Publishing
```bash
# Build distribution
python setup.py sdist

# Install locally for testing
pip install -e .

# Publish to PyPI (requires credentials)
python -m twine upload dist/*
```

### Running Tests
```bash
python -m pytest iaklogger/test_iaklogger.py -v
```

## Design Philosophy

- **Simplicity First**: Easy to start using with minimal configuration
- **Tag-Based Control**: Flexible filtering without complex logging levels
- **Drop-in Replacement**: Works alongside or instead of standard logging
- **No Configuration Required**: Works out of the box with sensible defaults
- **Rich Output Optional**: Enhanced formatting available but not required

## Common Patterns

### Module-Level Logging
```python
import iaklogger as lg
lg.register_self("cyan")  # Auto-detects module name
lg.log("Module initialized")
```

### Feature Toggle Logging
```python
lg.OPTIONS.unmuted_tags = ["FEATURE_X"]
lg.log("Debug info", tags=["FEATURE_X", "DEBUG"])
```

### Production vs Development
```python
# Development: verbose
lg.OPTIONS.unmuted_tags = []  # Allow all
lg.OPTIONS.show_tags = True
lg.OPTIONS.show_time = True

# Production: minimal
lg.OPTIONS.unmuted_tags = ["ERROR", "WARNING"]
lg.OPTIONS.log_file = "/var/log/myapp.log"
```

## Known Issues & Limitations

- Alpha stage software, API may change
- No async logging support
- File logging is synchronous (may block on I/O)
- Progress tracking requires Rich library
- No remote logging support
- No structured logging (JSON, etc.)

## Future Considerations

Based on the current implementation, potential improvements could include:
- Async file I/O for better performance
- Structured log output formats
- Log rotation instead of truncation
- Context managers for temporary tag changes
- Remote logging backends
- Performance profiling utilities
