import json
import re


def json_to_js_object(json_string, variable_name="eventData", export_default=True):
    """
    Convert a JSON string to JavaScript object code.
    
    Args:
        json_string (str): The JSON string to convert
        variable_name (str): The name of the JavaScript variable (default: "linksData")
        export_default (bool): Whether to add "export default" statement (default: True)
    
    Returns:
        str: JavaScript object code
    """
    try:
        # Parse the JSON string
        data = json.loads(json_string)

        # Convert to JavaScript format
        js_code = json_to_js_format(data, 0)

        # Create the complete JavaScript code
        result = f"const {variable_name} = {js_code};\n"

        if export_default:
            result += f"\nexport default {variable_name};"

        return result

    except json.JSONDecodeError as e:
        return f"Error parsing JSON: {e}"


def json_to_js_format(obj, indent_level=0):
    """
    Recursively convert Python objects to JavaScript format string.
    
    Args:
        obj: The object to convert
        indent_level (int): Current indentation level
    
    Returns:
        str: JavaScript formatted string
    """
    indent = "  " * indent_level
    next_indent = "  " * (indent_level + 1)

    if isinstance(obj, dict):
        if not obj:
            return "{}"

        items = []
        for key, value in obj.items():
            # Convert key to JavaScript property format (no quotes for valid identifiers)
            if is_valid_js_identifier(key):
                js_key = key
            else:
                js_key = f'"{key}"'

            js_value = json_to_js_format(value, indent_level + 1)
            items.append(f"{next_indent}{js_key}: {js_value}")

        return "{\n" + ",\n".join(items) + "\n" + indent + "}"

    elif isinstance(obj, list):
        if not obj:
            return "[]"

        items = []
        for item in obj:
            js_item = json_to_js_format(item, indent_level + 1)
            items.append(f"{next_indent}{js_item}")

        return "[\n" + ",\n".join(items) + "\n" + indent + "]"

    elif isinstance(obj, str):
        # Escape quotes and special characters
        escaped = obj.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t',
                                                                                                                  '\\t')
        return f'"{escaped}"'

    elif isinstance(obj, bool):
        return "true" if obj else "false"

    elif obj is None:
        return "null"

    else:
        # Numbers and other types
        return str(obj)


def is_valid_js_identifier(name):
    """
    Check if a string is a valid JavaScript identifier.
    
    Args:
        name (str): The string to check
    
    Returns:
        bool: True if valid identifier, False otherwise
    """
    # JavaScript identifier regex pattern
    pattern = r'^[a-zA-Z_$][a-zA-Z0-9_$]*$'
    return bool(re.match(pattern, name)) and name not in ['class', 'const', 'let', 'var', 'function', 'return', 'if',
                                                          'else', 'for', 'while', 'do', 'switch', 'case', 'default',
                                                          'break', 'continue', 'try', 'catch', 'finally', 'throw',
                                                          'new', 'this', 'super', 'extends', 'import', 'export', 'from',
                                                          'as', 'async', 'await', 'yield', 'static', 'public',
                                                          'private', 'protected']
