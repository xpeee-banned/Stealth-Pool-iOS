#!/usr/bin/env python3
import os, json, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))

def check(what, path):
    if not os.path.exists(path):
        print(f"  [WARN] {what} no encontrado"); return
    if path.endswith('.js'):
        r = subprocess.run(["node", "--check", path], capture_output=True, text=True)
        if r.returncode == 0: print(f"  [OK] {what} syntax OK")
        else: print(f"  [FAIL] {what}: {r.stderr.strip()}")
    else:
        sz = os.path.getsize(path)
        print(f"  [OK] {what} ({sz}B)")

def main():
    print("\n=== STEALTH POOL - HEALTH CHECK ===\n")
    check("Discord Bot", os.path.join(BASE, "discord-bot", "index.js"))
    check("Desktop", os.path.join(BASE, "desktop", "bot.js"))
    check("db.json", os.path.join(BASE, "discord-bot", "db.json"))
    check("ipa_builder.py", os.path.join(BASE, "ios", "ipa_builder.py"))
    check("stealth_ios.js", os.path.join(BASE, "ios", "stealth_ios.js"))
    apk = r"C:\Users\marti\Downloads\8 ball pool proyects\proyect apk\proyect apk\FluxPro-debug.apk.tmp"
    if os.path.exists(apk):
        mb = os.path.getsize(apk) / (1024*1024)
        print(f"  [OK] APK pre-compilado ({mb:.1f}MB)")
    else:
        print("  [WARN] APK no encontrado")
    print("\n=== CHECK COMPLETE ===")

if __name__ == "__main__":
    main()