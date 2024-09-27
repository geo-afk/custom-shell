# File Operations CLI Tool

A command-line interface tool for performing various file operations across different operating systems (Windows, Linux, and macOS).

## Features

- Cross-platform support (Windows, Linux, macOS)
- File operations:
  - Create files
  - Delete files
  - Rename files
- Command piping
- Interactive help system
- Support for multiple file extensions (.txt, .pdf, .docx)

## Installation

##### 1. Ensure you have Python 3.x installed on your system
##### 2. Clone this repository:
```bash
git clone https://github.com/geo-afk/custom-shell.git
cd file-operations-cli
pip install pydantic: 2.9.2
```

## Usage

Run the program:
```bash
python main.py
```

### Available Commands

- `create <filename>` - Create a new file
- `delete <filename>` - Delete an existing file
- `rename <filename>` - Rename an existing file (prompts for new name)
- `help` - Display general help information
- `help <command>` - Display help for a specific command
- `c` - Clear the screen
- `e` - Exit the program

### Command Piping

The tool supports basic command piping using `<`, `>`, and `|` operators.

### Examples

```bash
>> create test.txt
>> rename test.txt
Enter new filename: newtest.txt
>> delete newtest.txt
```

## Project Structure

- `main.py` - Entry point and main program loop
- `compute.py` - Handles execution of file operations
- `input_parser.py` - Parses and validates user input
- `help_parser.py` - Manages the help system
- `.\static\constant_types.py` - Defines constants, enums, and type definitions
- `\static\exceptions` - Defination of custom exceptions 
- `static\help.json` - Strores the help details for command `General` `Specific`

## Technical Details

### Dependencies

- Python 3.x
- Pydantic (for data validation)

### Key Components

##### 1. **Platform Detection**
   - Automatically detects the operating system
   - Adjusts commands based on the platform

##### 2. **Input Validation**
   - Validates file extensions
   - Checks for valid operations
   - Parses piped commands

##### 3. **Error Handling**
   - Custom exceptions for various error scenarios
   - User-friendly error messages

##### 4. **Help System**
   - JSON-based help content
   - Context-sensitive help for each command

## Error Handling

The tool uses custom exceptions:
- `InvalidCommand` - For invalid user inputs
- `FileOperationError` - For file-related errors
- `CommonException` - For general errors

## Extending the Tool

To add new file operations:
##### 1. Add the operation to `FileOperation` enum in `constant_types.py`
##### 2. Add corresponding commands for each platform in `FILE_OPERATIONS`
##### 3. Update the help system in the JSON file
##### 4. Implement any necessary validation in `InputParserAndValidator`

## Limitations

- Limited to basic file operations
- Supports only .txt, .pdf, and .docx file extensions
- Basic command piping functionality

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license information here]

