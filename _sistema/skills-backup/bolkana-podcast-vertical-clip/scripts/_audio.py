import os, subprocess, shutil, numpy as np
def root(start=None):
    """Bolkana podcast root: the first folder upwards (from start, then cwd) that holds _sistema/. Override: BOLKANA_ROOT."""
    if os.environ.get("BOLKANA_ROOT"): return os.environ["BOLKANA_ROOT"]
    for s in (start, os.getcwd()):
        d = os.path.abspath(s) if s else None
        while d and d != "/":
            if os.path.isdir(os.path.join(d, "_sistema")): return d
            d = os.path.dirname(d)
    raise SystemExit("no encuentro la carpeta del podcast (con _sistema/); ejecuta desde ella o define BOLKANA_ROOT")
def music_lib(start=None): return os.environ.get("BOLKANA_MUSIC") or os.path.join(root(start), "_sistema", "musica")
def _ff():
    try:
        c = os.path.join(root(), "_sistema/tools/bin/ffmpeg")
        if os.path.exists(c): return c
    except SystemExit: pass
    c = shutil.which("ffmpeg")
    if c: return c
    raise SystemExit("ffmpeg not found")
FF = os.environ.get("FFMPEG") or _ff()
def load(f, sr, ss=None, t=None):
    cmd = [FF, "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + (["-t", str(t)] if t is not None else []) + ["-i", f, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, dtype=np.float32)
