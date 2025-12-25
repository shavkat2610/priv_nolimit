from Cocoa import NSObject
from AppKit import NSWindow, NSTitledWindowMask, NSClosableWindowMask, NSMiniaturizableWindowMask, NSBackingStoreType, NSSlider, NSApplication

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        # Erstelle ein Fenster
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            ((200, 200), (400, 200)),  # Position und Größe
            NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask,
            NSBackingStoreType.NSBackingStoreBuffered,
            False
        )
        self.window.setTitle_("NSSlider Beispiel")
        
        # Erstelle einen Slider
        self.slider = NSSlider.alloc().initWithFrame_(((50, 50), (300, 30)))
        self.slider.setMinValue_(0.0)
        self.slider.setMaxValue_(100.0)
        self.slider.setDoubleValue_(50.0)  # Startwert
        self.slider.setTarget_(self)
        self.slider.setAction_("sliderChanged:")
        
        # Füge den Slider zum Fenster hinzu
        self.window.contentView().addSubview_(self.slider)
        self.window.makeKeyAndOrderFront_(None)
    
    def sliderChanged_(self, sender):
        value = sender.doubleValue()
        print(f"Slider-Wert: {value}")

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.run()



