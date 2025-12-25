


from AppKit import NSApplication, NSApp, NSWorkspace
from Quartz import kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGWindowListCopyWindowInfo
import time

workspace = NSWorkspace.sharedWorkspace()
activeApps = workspace.runningApplications()
# print(activeApps)
# exit()

time.sleep(10) 




def minimize_client():
    for app in activeApps:
         if app.localizedName()=="GGPoker":
              app.hide()

# minimize_client()

for app in activeApps:
    if app.localizedName()=="GGPoker":
        break

# app.hide()

time.sleep(5)
from Cocoa import NSApplicationActivateIgnoringOtherApps, NSApplicationActivateAllWindows

app.unhide()

app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)


time.sleep(15)
# or 
app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps | NSApplicationActivateAllWindows)