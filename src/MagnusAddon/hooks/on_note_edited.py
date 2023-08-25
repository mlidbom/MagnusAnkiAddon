from aqt import gui_hooks

from note.mynote import MyNote


def init() -> None:
    # noinspection PyProtectedMember
    gui_hooks.editor_did_fire_typing_timer.append(MyNote._on_note_edited)