#!/usr/bin/env python3
# Stealth Pool iOS IPA Builder v2.0
import os, sys, shutil, tempfile, zipfile, struct

VERSION = "2.0"
GADGET = "FridaGadget.dylib"
OUTPUT = "8BallPool-Stealth.ipa"

def e(m): print(f"[ERROR] {m}"); sys.exit(1)
def i(m): print(f"[INFO] {m}")
def o(m): print(f"[OK] {m}")

def dl_gadget():
    import urllib.request
    url = "https://github.com/frida/frida/releases/download/16.2.1/frida-gadget-16.2.1-ios-universal.dylib"
    if os.path.exists(GADGET): i("FridaGadget ya existe"); return
    i("Descargando FridaGadget (120MB)...")
    try:
        urllib.request.urlretrieve(url, GADGET)
        o("Descargado!")
    except Exception as ex:
        e(f"Fallo descarga: {ex}\nManual: {url}")

def make_config():
    with open("stealth_config.plist", "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
        f.write('<plist version="1.0"><dict><key>interaction</key><dict>')
        f.write('<key>type</key><string>script</string>')
        f.write('<key>path</key><string>stealth_ios.js</string>')
        f.write('</dict></dict></plist>\n')
    o("Config creado")

def extract(ipa, out):
    with zipfile.ZipFile(ipa) as z: z.extractall(out)

def find_app(payload):
    for item in os.listdir(payload):
        if item.endswith(".app"): return os.path.join(payload, item)
    e("No .app found")

def patch_macho(binp, dylib):
    with open(binp, "rb") as f: data = bytearray(f.read())
    mag = struct.unpack_from("<I", data, 0)[0]
    is64 = mag == 0xFEEDFACF
    if not (is64 or mag == 0xFEEDFACE): e(f"Bad Mach-O: {hex(mag)}")
    hdr = 32 if is64 else 28
    ncmds = struct.unpack_from("<I", data, 16)[0]
    szcmds = struct.unpack_from("<I", data, 20)[0]
    dpath = dylib.encode() + b"\x00"
    while len(dpath) % 8: dpath += b"\x00"
    cmdsz = 24 + len(dpath)
    new = struct.pack("<II", 0xC, cmdsz)
    new += struct.pack("<IIII", 24, 2, 0x10000, 0x10000)
    new += dpath
    data[hdr:hdr] = new
    struct.pack_into("<I", data, 16, ncmds+1)
    struct.pack_into("<I", data, 20, szcmds+cmdsz)
    c = hdr
    for _ in range(ncmds+1):
        cmd = struct.unpack_from("<I", data, c)[0]
        sz = struct.unpack_from("<I", data, c+4)[0]
        if cmd == 0x1C:
            doff = struct.unpack_from("<I", data, c+8)[0]
            dsz = struct.unpack_from("<I", data, c+12)[0]
            for i in range(doff, min(doff+dsz, len(data))): data[i] = 0
            for i in range(c, c+16): data[i] = 0
            break
        c += sz
    with open(binp, "wb") as f: f.write(bytes(data))
    o(f"Patched: {dylib}")

def inject(ab):
    i("Injecting FridaGadget...")
    fw = os.path.join(ab, "Frameworks")
    os.makedirs(fw, exist_ok=True)
    shutil.copy2(GADGET, os.path.join(fw, GADGET))
    shutil.copy2("stealth_ios.js", os.path.join(ab, "stealth_ios.js"))
    make_config()
    shutil.copy2("stealth_config.plist", os.path.join(ab, "stealth_config.plist"))
    import plistlib
    exe = None
    try:
        with open(os.path.join(ab, "Info.plist"), "rb") as f:
            exe = plistlib.load(f).get("CFBundleExecutable")
    except: pass
    if not exe:
        cands = [(fn, os.path.getsize(os.path.join(ab, fn)))
                 for fn in os.listdir(ab)
                 if os.path.isfile(os.path.join(ab, fn))
                 and not fn.endswith((".plist", ".png", ".js", ".dylib"))
                 and os.path.getsize(os.path.join(ab, fn)) > 1000000]
        if cands: exe = max(cands, key=lambda x: x[1])[0]
    if not exe: e("Executable not found")
    binp = os.path.join(ab, exe)
    i(f"Binary: {binp}")
    patch_macho(binp, f"@executable_path/Frameworks/{GADGET}")
    o("Injection done!")

def repack(src, dst):
    if os.path.exists(dst): os.remove(dst)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src):
            for f in files:
                fp = os.path.join(root, f)
                an = os.path.relpath(fp, src)
                if "__MACOSX" not in an and ".DS_Store" not in an:
                    z.write(fp, an)
    mb = os.path.getsize(dst) / (1024*1024)
    o(f"IPA: {dst} ({mb:.1f} MB)")

def main():
    print(f"\n  STEALTH POOL iOS IPA BUILDER v{VERSION}\n")
    if len(sys.argv) > 1:
        if sys.argv[1] == "--download": dl_gadget(); return
        if sys.argv[1] in ("--help", "-h"):
            print("Usage: python ipa_builder.py [--download|--guide]"); return
        if sys.argv[1] == "--guide":
            print("""
1. Obtener IPA original (Sideloadly > Download from device)
2. python ipa_builder.py --download
3. python ipa_builder.py -> 8BallPool-Stealth.ipa
4. Instalar con Sideloadly en iPhone
5. Tocar 3x logo Miniclip -> menu -> ingresar key
"""); return
    ipa = next((os.path.abspath(f) for f in os.listdir(".") if f.endswith(".ipa")), None)
    if not ipa: e("No .ipa found")
    i(f"IPA: {ipa}")
    if not os.path.exists(GADGET): dl_gadget()
    if not os.path.exists("stealth_ios.js"): e("Missing stealth_ios.js")
    tmp = tempfile.mkdtemp(prefix="stealth_")
    try:
        extract(ipa, tmp)
        pl = next((os.path.join(tmp, d) for d in os.listdir(tmp) if d.startswith("Payload")), None)
        if not pl: e("No Payload dir")
        app = find_app(pl)
        i(f"Bundle: {app}")
        inject(app)
        repack(tmp, OUTPUT)
        print(f"\n>>> DONE: {OUTPUT}")
    finally:
        if os.path.exists(tmp): shutil.rmtree(tmp)

if __name__ == "__main__":
    main()