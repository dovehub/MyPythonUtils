# android: from airtest.core.android import Android
import time


def lock_screen(android):
    if android.is_screenon():
        android.keyevent("26")


def unlock_screen(android):
    if not android.is_screenon():
        android.wake()
        time.sleep(2)
    if not (android.is_screenon() and not android.is_locked()):
        if not android.is_screenon():
            android.keyevent("26")
            android.unlock()
        if android.is_locked():
            android.unlock()
        time.sleep(2)
