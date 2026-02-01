from __future__ import annotations

from typing import TYPE_CHECKING

from jastudio.sysutils.typed import checked_cast, non_optional
from PyQt6.QtCore import pyqtBoundSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QInputDialog, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

if TYPE_CHECKING:
    from collections.abc import Callable

    from jastudio.note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper

class StringChipWidget(QFrame):
    """A chip widget displaying a string with an X button to remove it."""

    def __init__(self, text: str, on_remove: Callable[[],None]) -> None:
        super().__init__()
        self.text: str = text

        # Style the chip
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            StringChipWidget {
                background-color: #e0e0e0;
                border-radius: 3px;
                padding: 2px;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(4)

        # Add label
        label = QLabel(text)
        layout.addWidget(label)

        # Add remove button (X)
        remove_btn = QPushButton("×")
        remove_btn.setMaximumSize(16, 16)
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #666;
                font-weight: bold;
                font-size: 14px;
                padding: 0px;
            }
            QPushButton:hover {
                color: #ff0000;
            }
        """)
        checked_cast(pyqtBoundSignal, remove_btn.clicked).connect(on_remove)  # pyright: ignore[reportUnknownMemberType]
        layout.addWidget(remove_btn)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

class FlowLayout(QWidget):
    """A widget that lays out children in a horizontal flow, wrapping to new lines as needed."""

    def __init__(self) -> None:
        super().__init__()
        self.items: list[QWidget] = []
        self.main_layout:QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(4)
        self.setLayout(self.main_layout)
        self._current_row: QHBoxLayout | None = None

    def add_widget(self, widget: QWidget) -> None:
        """Add a widget to the flow layout."""
        self.items.append(widget)
        self._rebuild()

    def clear(self) -> None:
        """Remove all widgets."""
        for item in self.items:
            item.deleteLater()
        self.items.clear()
        self._rebuild()

    def _rebuild(self) -> None:
        """Rebuild the layout."""
        # Clear existing layout
        while self.main_layout.count():
            child = non_optional(self.main_layout.takeAt(0))
            if child.widget():
                non_optional(child.widget()).setParent(None)  # type: ignore

        # Create new rows and add items
        if self.items:
            current_row = QHBoxLayout()
            current_row.setSpacing(4)

            for item in self.items:
                current_row.addWidget(item)

            current_row.addStretch()
            self.main_layout.addLayout(current_row)

        self.main_layout.addStretch()

class StringSetWidget(QWidget):
    """Widget for editing a set of strings with add/remove functionality displayed as chips."""

    def __init__(self, field: FieldSetWrapper[str], title: str, on_change_callback: Callable[[],None] | None = None) -> None:
        super().__init__()
        self.field: FieldSetWrapper[str] = field
        self.title: str = title
        self.on_change_callback: Callable[[],None] | None = on_change_callback

        # Main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Add title label (bold)
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold;")
        title_label.setMinimumWidth(120)
        main_layout.addWidget(title_label)

        # Create add button
        add_button = QPushButton("+ Add...")
        add_button.setMaximumWidth(80)
        checked_cast(pyqtBoundSignal, add_button.clicked).connect(self._on_add)  # pyright: ignore[reportUnknownMemberType]
        main_layout.addWidget(add_button)

        # Create flow layout to display chips
        self.flow_layout:FlowLayout = FlowLayout()
        self._refresh_chips()
        main_layout.addWidget(self.flow_layout)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def _refresh_chips(self) -> None:
        """Refresh the chip widgets with current values."""
        self.flow_layout.clear()
        for value in sorted(self.field.get()):
            chip = StringChipWidget(value, lambda _checked=None, v=value: self._remove_value(v))
            self.flow_layout.add_widget(chip)

    def _remove_value(self, value: str) -> None:
        """Remove a value from the set."""
        self.field.remove(value)
        self._refresh_chips()
        if self.on_change_callback:
            self.on_change_callback()

    def _on_add(self) -> None:
        """Handle add button click."""
        text, ok = QInputDialog.getText(self, f"Add to {self.title}", "Enter value:")
        if ok and text:
            self.field.add(text)
            self._refresh_chips()
            if self.on_change_callback:
                self.on_change_callback()
