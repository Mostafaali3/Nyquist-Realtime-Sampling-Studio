from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon

signals_map = {}
is_signal_shown = {}

def add_signal(grid_layout, number):

    hide_icon = QIcon("icons_setup/icons/hide.png")
    delete_icon = QIcon("icons_setup/icons/delete.png")

    # Create a new horizontal layout for the component
    signals_layout = QHBoxLayout()
    signals_layout.setObjectName(f"signalLayout{number}")

    # Create label layout
    signal_label_layout = QHBoxLayout()
    signal_label = QLabel(f"Signal {number}")
    signal_label.setObjectName(f"signalLabel{number}")
    signal_label.setMaximumHeight(50)
    signal_label.setMinimumHeight(50)
    signal_label.setStyleSheet("""
        border: none;
        font-size: 12px;
        margin: 0;
        margin-left: 10px;
    """)
    signal_label_layout.addWidget(signal_label)

    # Create buttons layout
    signal_buttons_layout = QHBoxLayout()
    spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

    show_button = QPushButton()
    show_button.setIcon(hide_icon)
    show_button.setObjectName(f"signalShowButton{number}")
    show_button.setMaximumSize(40, 40)
    show_button.setMinimumSize(40, 40)
    show_button.setStyleSheet("""
        border: none;
        margin: 0;
    """)
    # show_button.clicked.connect(lambda: show_hide_signal(show_button, number))

    delete_button = QPushButton()
    delete_button.setIcon(delete_icon)
    delete_button.setObjectName(f"signalDeleteButton{number}")
    delete_button.setMaximumSize(40, 40)
    delete_button.setMinimumSize(40, 40)
    delete_button.setStyleSheet("""
        border: none;
        margin: 0;
    """)
    # delete_button.clicked.connect(lambda: delete_signal(grid_layout, number))

    # Add widgets to component_buttons_layout
    signal_buttons_layout.addSpacerItem(spacer)
    signal_buttons_layout.addWidget(show_button)
    signal_buttons_layout.addWidget(delete_button)

    # Add label and buttons layouts to the main component layout
    signals_layout.addLayout(signal_label_layout)
    signals_layout.addLayout(signal_buttons_layout)

    # Add component layout to the grid layout in componentsContainerWidget
    row_position = grid_layout.rowCount()  # Place new component in the next row
    grid_layout.addLayout(signals_layout, row_position, 0)
    signals_map[number] = signals_layout
    is_signal_shown[number] = True  # Initialize the visibility state


def clear_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clear_layout(item.layout())

def delete_signal(grid_layout, number):
    # Check if the component exists in the map
    if number in signals_map:
        # Get the layout to delete
        signal_layout = signals_map[number]

        # Clear the layout
        clear_layout(signal_layout)

        # Remove the layout from the grid layout
        grid_layout.removeItem(signal_layout)

        # Delete the component layout itself
        signal_layout.setParent(None)
        signal_layout.deleteLater()

        # Remove the entry from the components_map
        del signals_map[number]
        del is_signal_shown[number]

        # Optionally, you can update the grid layout if needed
        # For example, you could adjust the layout after deletion
        grid_layout.invalidate()  # Re-layout the grid
    else:
        print(f"Component {number} not found.")


def show_signal(signal_button, number):
    hide_icon = QIcon("icons_setup/icons/hide.png")

    if number in is_signal_shown:
        is_signal_shown[number] = True
        signal_button.setIcon(hide_icon)


def hide_signal(signal_button, number):
    show_icon = QIcon("icons_setup/icons/show.png")

    if number in is_signal_shown:
        is_signal_shown[number] = False
        signal_button.setIcon(show_icon)


def show_hide_signal(signal_button, number):

    show_icon = QIcon("icons_setup/icons/show.png")
    hide_icon = QIcon("icons_setup/icons/hide.png")

    if number in is_signal_shown:
        is_signal_shown[number] = not is_signal_shown[number]
        if is_signal_shown[number]:
            signal_button.setIcon(hide_icon)
        else:
            signal_button.setIcon(show_icon)

