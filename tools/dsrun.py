"""Headless DuckStation run: Xvfb + XTest key presses + periodic screenshots.

python3 dsrun.py CUE --out DIR --route "1500 -;6 start;..." [--shot-every SEC] [--card CARD.mcd] [--tail SEC]
Route steps are "FRAMES BUTTON" like emu.py (- = idle). Buttons: up down left right cross circle square triangle start select.
Frames are converted to wall-clock time at 60 fps (EmulationSpeed = 1).
"""
import argparse, ctypes, os, shutil, subprocess, sys, threading, time

DS = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(DS, "squashfs-root", "AppRun")
KEYS = {"up": "Up", "down": "Down", "left": "Left", "right": "Right", "cross": "k", "circle": "l",
        "square": "j", "triangle": "i", "start": "Return", "select": "BackSpace"}

ap = argparse.ArgumentParser()
ap.add_argument("cue"); ap.add_argument("--out", required=True); ap.add_argument("--route", required=True)
ap.add_argument("--shot-every", type=float, default=2.5); ap.add_argument("--card")
ap.add_argument("--tail", type=float, default=0, help="extra seconds after the route")
ap.add_argument("--display", default=":77")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
if a.card:
    shutil.copy(a.card, os.path.join(DS, "card.mcd"))

env = dict(os.environ, DISPLAY=a.display,  
           QT_QPA_PLATFORM="xcb")
xvfb = subprocess.Popen(["Xvfb", a.display, "-screen", "0", "1024x768x24", "-nolisten", "tcp"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
log = open(os.path.join(a.out, "ds.log"), "w")
ds = subprocess.Popen([APP, "-batch", "-fastboot", "--", os.path.abspath(a.cue)], env=env, stdout=log, stderr=log)

x11 = ctypes.CDLL("libX11.so.6"); xt = ctypes.CDLL("libXtst.so.6")
x11.XOpenDisplay.restype = ctypes.c_void_p
x11.XStringToKeysym.restype = ctypes.c_ulong
x11.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
xt.XTestFakeKeyEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int, ctypes.c_ulong]
xt.XTestFakeMotionEvent.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_ulong]
xt.XTestFakeButtonEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int, ctypes.c_ulong]
x11.XFlush.argtypes = [ctypes.c_void_p]
dpy = x11.XOpenDisplay(a.display.encode())
if not dpy:
    sys.exit("no display")

def key(name, down):
    kc = x11.XKeysymToKeycode(dpy, x11.XStringToKeysym(KEYS[name].encode()))
    xt.XTestFakeKeyEvent(dpy, kc, 1 if down else 0, 0); x11.XFlush(dpy)

stop = False
def shooter():
    i = 0; t0 = time.time()
    while not stop:
        t = time.time() - t0
        subprocess.run(["import", "-display", a.display, "-window", "root",
                        os.path.join(a.out, "t%05.1f.png" % t)], stderr=subprocess.DEVNULL)
        i += 1
        time.sleep(max(0, a.shot_every - (time.time() - t0 - t)))

time.sleep(4)  # window up
# put the pointer on the window and click so the display widget has keyboard focus
xt.XTestFakeMotionEvent(dpy, -1, 300, 300, 0); xt.XTestFakeButtonEvent(dpy, 1, 1, 0); xt.XTestFakeButtonEvent(dpy, 1, 0, 0)
x11.XFlush(dpy)
th = threading.Thread(target=shooter, daemon=True); th.start()
try:
    for step in a.route.split(";"):
        step = step.strip()
        if not step:
            continue
        n, b = step.split(None, 1)
        secs = int(n) / 60.0
        if b == "-":
            time.sleep(secs); continue
        btns = b.split("+")
        for k in btns: key(k, True)
        time.sleep(max(secs, 0.1))
        for k in btns: key(k, False)
        time.sleep(0.05)
    time.sleep(a.tail)
finally:
    stop = True; time.sleep(0.5)
    subprocess.run(["import", "-display", a.display, "-window", "root", os.path.join(a.out, "final.png")], stderr=subprocess.DEVNULL)
    ds.terminate()
    try: ds.wait(5)
    except subprocess.TimeoutExpired: ds.kill()
    xvfb.terminate()
print("done", a.out)
