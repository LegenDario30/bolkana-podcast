#!/usr/bin/env python3
"""Cut several fragments of a long master (full podcast episode) and join them into one clip source.

Usage:
  python3 cut_fragments.py --master "assets/<episode>.mp4" --words <episode_words.json> \
      --fragments fragments.json --root <batch dir> [--offset -0.06] [clip_01 clip_02 ...]

fragments.json: {"clip_01": {"slug": "...", "title": "...", "frags": [{"id": "a", "start": 124.0, "end": 137.42}, ...]}, ...}
  start/end are the first/last word times in the WORDS timeline (whole-episode whisper run).
--offset: seconds to add when seeking the master if it is a different encode than the one the words were
  transcribed from (e.g. a re-exported HD master that runs 0.06 s earlier -> -0.06).
Each fragment gets 0.3 s handles, is re-encoded frame-exact at the master's native size (or --height), 25 fps, CRF 10, with 20 ms
audio fades, and the fragments are concatenated in order. Writes, per clip:
  <root>/<clip>/media/<clip>_joined.mp4
  <root>/<clip>/clip/transcript.json        clip-local words [{text,start,end,src,frag,id}] (no re-transcription)
  <root>/<clip>/clip/fragments_plan.json    where every fragment landed in the joined file
"""
import json, subprocess, os, sys, argparse
ap = argparse.ArgumentParser()
ap.add_argument("--master", required=True); ap.add_argument("--words", required=True)
ap.add_argument("--fragments", required=True); ap.add_argument("--root", required=True)
ap.add_argument("--offset", type=float, default=0.0); ap.add_argument("--fps", default="25")
ap.add_argument("--preset", default="slow", help="x264 preset (fast is ~2x quicker for working copies)")
ap.add_argument("--height", type=int, default=0, help="scale the working copy to this height (e.g. 1440 for a 4K master); 0 = native")
ap.add_argument("clips", nargs="*")
A = ap.parse_args(); M = 0.3
F = json.load(open(A.fragments)); W = json.load(open(A.words))
for clip, c in F.items():
    if A.clips and clip not in A.clips: continue
    fc = []; ins = []; inputs = []; off = 0; plan = []; words = []
    fr = c["frags"]
    for i, f in enumerate(fr):
        a = round(f["start"] - M, 3); b = round(f["end"] + M, 3)
        # handles must not overlap a source-adjacent neighbour, or the same audio plays twice at the join
        if i > 0 and fr[i-1]["end"] <= f["start"] < fr[i-1]["end"] + 2 * M: a = round((fr[i-1]["end"] + f["start"]) / 2, 3)
        if i + 1 < len(fr) and f["end"] <= fr[i+1]["start"] < f["end"] + 2 * M: b = round((f["end"] + fr[i+1]["start"]) / 2, 3)
        d = round(b - a, 3)
        inputs += ["-ss", f"{a + A.offset:.3f}", "-t", f"{d}", "-i", A.master]
        sc = f"scale=-2:{A.height}:flags=lanczos," if A.height else ""
        fc.append(f"[{i}:v]setpts=PTS-STARTPTS,fps={A.fps},{sc}trim=duration={d},format=yuv420p[v{i}];"
                  f"[{i}:a]asetpts=PTS-STARTPTS,aresample=48000,atrim=duration={d},afade=t=in:d=0.02,afade=t=out:st={d-0.02:.3f}:d=0.02[a{i}];")
        ins.append(f"[v{i}][a{i}]")
        for w in W:
            if a <= w["start"] < b:
                words.append({"text": w["text"], "start": round(w["start"] - a + off, 3), "end": round(min(w["end"], b) - a + off, 3),
                              "src": w["start"], "frag": f["id"], "id": "w%d" % len(words)})
        plan.append({**f, "cutIn": a, "cutOut": b, "seekMaster": round(a + A.offset, 3), "clipStart": round(off, 3), "clipEnd": round(off + d, 3)})
        off += d
    fc = "".join(fc) + "".join(ins) + f"concat=n={len(ins)}:v=1:a=1[v][a]"
    for sub in ("media", "clip"): os.makedirs(os.path.join(A.root, clip, sub), exist_ok=True)
    out = os.path.join(A.root, clip, "media", f"{clip}_joined.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", A.preset,
                    "-crf", "10", "-tune", "film", "-g", "25", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    json.dump(words, open(os.path.join(A.root, clip, "clip", "transcript.json"), "w"), ensure_ascii=False, indent=1)
    json.dump(plan, open(os.path.join(A.root, clip, "clip", "fragments_plan.json"), "w"), ensure_ascii=False, indent=1)
    print(clip, round(off, 3), [(p["id"], p["seekMaster"], p["clipStart"]) for p in plan])
