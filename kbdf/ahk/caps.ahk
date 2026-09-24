#Requires AutoHotkey v2.0
; Optional: CapsLock as manual Alt+Shift layout toggle.
; Shift+CapsLock still toggles CapsLock.
; kbdf on Windows switches layout via WinAPI and does not need this script.

SetCapsLockState "AlwaysOff"
+CapsLock::CapsLock
CapsLock::Send "{Alt down}{Shift down}{Shift up}{Alt up}"
