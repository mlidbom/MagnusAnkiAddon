from __future__ import annotations

from typing import TYPE_CHECKING

from jastudio.sysutils.typed import checked_cast
from PyQt6.QtCore import pyqtBoundSignal
from PyQt6.QtWidgets import QButtonGroup, QHBoxLayout, QRadioButton, QWidget

if TYPE_CHECKING:
    from collections.abc import Callable

    from jastudio.note.notefields.require_forbid_flag_field import RequireForbidFlagField

class RequireForbidWidget(QWidget):
    """Widget for editing a require/forbid flag field with three radio buttons."""

    def __init__(self, field: RequireForbidFlagField, title: str, on_change_callback: Callable[[str, bool], None], reparse_trigger: bool = True) -> None:
        super().__init__()
        self.field: RequireForbidFlagField = field
        self.title: str = title
        self.on_change_callback: Callable[[str, bool], None] = on_change_callback
        self.reparse_trigger: bool = reparse_trigger

        # Set up layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Create radio buttons
        self.button_group: QButtonGroup = QButtonGroup(self)
        self.unset_radio: QRadioButton = QRadioButton("Unset")
        self.required_radio: QRadioButton = QRadioButton("Required")
        self.forbidden_radio: QRadioButton = QRadioButton("Forbidden")

        self.button_group.addButton(self.unset_radio, 0)
        self.button_group.addButton(self.required_radio, 1)
        self.button_group.addButton(self.forbidden_radio, 2)

        layout.addWidget(self.unset_radio)
        layout.addWidget(self.required_radio)
        layout.addWidget(self.forbidden_radio)

        self.setLayout(layout)

        # Set initial state and track it
        initial_required = field.is_configured_required
        initial_forbidden = field.is_configured_forbidden

        if initial_required:
            self.required_radio.setChecked(True)
            self.initial_state: int = 1
        elif initial_forbidden:
            self.forbidden_radio.setChecked(True)
            self.initial_state = 2
        else:
            self.unset_radio.setChecked(True)
            self.initial_state = 0

        # Connect signal
        checked_cast(pyqtBoundSignal, self.button_group.idClicked).connect(self._on_changed)  # pyright: ignore[reportUnknownMemberType]

    def _on_changed(self, button_id: int) -> None:
        # Update the field
        if button_id == 0:  # Unset
            if self.field.is_configured_required:
                self.field.set_required(False)
            if self.field.is_configured_forbidden:
                self.field.set_forbidden(False)
        elif button_id == 1:  # Required
            if not self.field.is_configured_required:
                self.field.set_required(True)
        elif button_id == 2:  # Forbidden
            if not self.field.is_configured_forbidden:
                self.field.set_forbidden(True)

        # Notify parent of change
        changed = (button_id != self.initial_state)
        self.on_change_callback(self.title, self.reparse_trigger and changed)
