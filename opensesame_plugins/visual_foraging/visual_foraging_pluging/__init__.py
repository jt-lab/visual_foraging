"""A docstring with a description of the plugin"""

# The category determines the group for the plugin in the item toolbar
category = "Visual Stimuli"

# Defines the auto-added GUI controls
# The custom widgets are in the example_custom_plugin.py
controls = [
    {
        "type": "checkbox",
        "var": "show_mousepointer",
        "label": "Show Mousepointer",
        "name": "show_mouse_pointer_widget",
        "tooltip": "Whether the mousepointer will be visible"
    }]

