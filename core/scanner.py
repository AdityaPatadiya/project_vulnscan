# core/scanner.py
import os
import importlib.util

def load_plugins():
    # Get absolute path to plugins directory relative to this file
    plugin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../plugins"))
    plugins = []

    # List all Python files in plugins directory
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            file_path = os.path.join(plugin_dir, filename)

            # Load module dynamically from file
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check if module has a scan function, then add to plugins list
            if hasattr(module, "scan"):
                plugins.append(module)

    return plugins

def run_plugins(plugins, urls):
    for plugin in plugins:
        plugin_name = plugin.__name__.upper()
        print(f"\n[+] Running {plugin_name} plugin...")
        for url in urls:
            plugin.scan(url)
