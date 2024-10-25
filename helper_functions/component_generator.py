from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon

components_map = {}

def add_component(grid_layout, number):

    edit_icon = QIcon("icons_setup/icons/edit.png")
    delete_icon = QIcon("icons_setup/icons/delete.png")

    # Create a new horizontal layout for the component
    component_layout = QHBoxLayout()
    component_layout.setObjectName(f"componentLayout{number}")

    # Create label layout
    component_label_layout = QHBoxLayout()
    component_label = QLabel(f"Component {number}")
    component_label.setObjectName(f"componentLabel{number}")
    component_label.setMaximumHeight(50)
    component_label.setMinimumHeight(50)
    component_label.setStyleSheet("""
        border: none;
        font-size: 12px;
        margin: 0;
        margin-left: 10px;
    """)
    component_label_layout.addWidget(component_label)

    # Create buttons layout
    component_buttons_layout = QHBoxLayout()
    spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

    edit_button = QPushButton()
    edit_button.setIcon(edit_icon)
    edit_button.setObjectName(f"componentEditButton{number}")
    edit_button.setMaximumSize(40, 40)
    edit_button.setMinimumSize(40, 40)
    edit_button.setStyleSheet("""
        border: none;
        margin: 0;
    """)

    delete_button = QPushButton()
    delete_button.setIcon(delete_icon)
    delete_button.setObjectName(f"componentDeleteButton{number}")
    delete_button.setMaximumSize(40, 40)
    delete_button.setMinimumSize(40, 40)
    delete_button.setStyleSheet("""
        border: none;
        margin: 0;
    """)

    # Add widgets to component_buttons_layout
    component_buttons_layout.addSpacerItem(spacer)
    component_buttons_layout.addWidget(edit_button)
    component_buttons_layout.addWidget(delete_button)

    # Add label and buttons layouts to the main component layout
    component_layout.addLayout(component_label_layout)
    component_layout.addLayout(component_buttons_layout)

    # Add component layout to the grid layout in componentsContainerWidget
    row_position = grid_layout.rowCount()  # Place new component in the next row
    grid_layout.addLayout(component_layout, row_position, 0)
    components_map[number] = component_layout


def delete_component(grid_layout, number):
    # Check if the component exists in the map
    if number in components_map:
        # Get the layout to delete
        component_layout = components_map[number]

        # Remove the layout from the grid layout
        grid_layout.removeItem(component_layout)

        # Remove all widgets from the layout and delete them
        for i in reversed(range(component_layout.count())): 
            widget = component_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Ensure the widget is deleted

        # Delete the component layout itself
        component_layout.deleteLater()

        # Remove the entry from the components_map
        del components_map[number]

        # Optionally, you can update the grid layout if needed
        # For example, you could adjust the layout after deletion
        grid_layout.invalidate()  # Re-layout the grid
    else:
        print(f"Component {number} not found.")

