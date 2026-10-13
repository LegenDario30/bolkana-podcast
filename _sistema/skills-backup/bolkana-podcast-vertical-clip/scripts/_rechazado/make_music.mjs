// Original music bed — deterministic synthesis (no samples, no external audio, no licence issues).
// Minimal lo-fi / modern: pad chords, sub bass, soft kick, snap, hats, pluck arp; drop + low hit on the climax word.
// Usage: node make_music.mjs <out.wav> --dur 34.3 --drop 32.05 --hit 32.66 [--bpm 100] [--seed 1337] [--style lofi|warm|lively|upbeat]
// Styles: lofi (original, chill, drums from bar 2) · warm (lofi groove from bar 1, arp early) · lively (brighter major-feel
// chords, four-on-the-floor kick, clap on 2&4, 16th hats, pumping pad, groove from 0 s) · upbeat (lively + offbeat open hats,
// harder pump, busier arp).
// Then: ffmpeg -i out.wav -af "lowpass=f=8000,aecho=0.8:0.5:60|110:0.25|0.18,afade=t=out:st=<dur-0.8>:d=0.75,loudnorm=I=-16:TP=-1.5" -b:a 192k bgm.mp3
import fs from "node:fs";
const arg = (k, d) => { const i = process.argv.indexOf("--" + k); return i > 0 ? parseFloat(process.argv[i + 1]) : d; };
const SR = 44100, DUR = arg("dur", 34.3), N = Math.floor(SR * DUR);
const L = new Float32Array(N), R = new Float32Array(N), PL = new Float32Array(N), PR = new Float32Array(N);
const SI = process.argv.indexOf("--style"), STYLE = SI > 0 ? process.argv[SI + 1] : "lofi";
const BRIGHT = STYLE === "lively" || STYLE === "upbeat", EARLY = STYLE !== "lofi";
const BPM = arg("bpm", 100), BEAT = 60 / BPM, BAR = BEAT * 4;
let seed = arg("seed", 1337); const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296) * 2 - 1;
const mtof = m => 440 * Math.pow(2, (m - 69) / 12);
const add = (i, l, r) => { if (i >= 0 && i < N) { L[i] += l; R[i] += r; } };
// chords: Am9, Fmaj7, Cmaj7, G6(add9)
const CH = BRIGHT ? [[53, 57, 60, 64, 67], [48, 55, 60, 64, 67], [57, 60, 64, 67, 72], [55, 59, 62, 67, 69]]   // Fmaj9, C(add9), Am7, G6
                 : [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [48, 55, 59, 64, 67], [55, 59, 62, 64, 69]];  // Am9, Fmaj7, Cmaj7, G6(add9)
const ROOT = BRIGHT ? [41, 48, 45, 43] : [45, 41, 48, 43];
const DROP = arg("drop", DUR - 2), HIT = arg("hit", DUR - 1.4); // drop before the climax word, hit on it
function pad(t0, dur, notes, g) {
  const s0 = Math.floor(t0 * SR), n = Math.floor(dur * SR);
  notes.forEach((m, k) => {
    const f = mtof(m), det = 1 + (k % 2 ? 0.0021 : -0.0017), pan = (k / (notes.length - 1)) * 0.8 - 0.4;
    let ph1 = 0, ph2 = 0;
    for (let i = 0; i < n; i++) {
      const t = i / SR, a = Math.min(1, t / 0.6) * Math.min(1, (dur - t) / 0.5);
      ph1 += f / SR; ph2 += f * det / SR;
      const v = (Math.sin(2 * Math.PI * ph1) + 0.35 * Math.sin(4 * Math.PI * ph2) + 0.12 * Math.sin(6 * Math.PI * ph1)) * a * g;
      const j = s0 + i; if (j >= 0 && j < N) { PL[j] += v * (0.5 - pan * 0.5); PR[j] += v * (0.5 + pan * 0.5); }
    }
  });
}
function bass(t0, dur, m, g) {
  const s0 = Math.floor(t0 * SR), n = Math.floor(dur * SR), f = mtof(m - 12);
  let ph = 0;
  for (let i = 0; i < n; i++) { const t = i / SR; ph += f / SR;
    const a = Math.min(1, t / 0.02) * Math.exp(-t * 1.6) * Math.min(1, (dur - t) / 0.05);
    const v = (Math.sin(2 * Math.PI * ph) + 0.25 * Math.sin(4 * Math.PI * ph)) * a * g; add(s0 + i, v, v); }
}
function kick(t0, g) {
  const s0 = Math.floor(t0 * SR); let ph = 0;
  for (let i = 0; i < SR * 0.45; i++) { const t = i / SR, f = 48 + 110 * Math.exp(-t * 28); ph += f / SR;
    const v = Math.sin(2 * Math.PI * ph) * Math.exp(-t * 7) * g; add(s0 + i, v, v); }
}
function snap(t0, g) {
  const s0 = Math.floor(t0 * SR); let lp = 0;
  for (let i = 0; i < SR * 0.22; i++) { const t = i / SR, nz = rnd(); lp += (nz - lp) * 0.35;
    const v = ((nz - lp) * 0.8 + Math.sin(2 * Math.PI * 190 * t) * 0.25) * Math.exp(-t * 24) * g; add(s0 + i, v * 0.9, v); }
}
function hat(t0, g, pan) {
  const s0 = Math.floor(t0 * SR); let prev = 0;
  for (let i = 0; i < SR * 0.06; i++) { const t = i / SR, nz = rnd(), hp = nz - prev; prev = nz;
    const v = hp * Math.exp(-t * 70) * g; add(s0 + i, v * (1 - pan), v * (1 + pan)); }
}
function clap(t0, g) {   // three quick noise bursts + a tail
  const s0 = Math.floor(t0 * SR); let lp = 0;
  for (let i = 0; i < SR * 0.25; i++) { const t = i / SR, nz = rnd(); lp += (nz - lp) * 0.5; const bp = nz - lp;
    const env = (t < 0.03 ? (Math.exp(-((t % 0.01) * 400))) : 0) * 0.6 + Math.exp(-t * 18) * 0.7;
    const v = bp * env * g; add(s0 + i, v * 0.95, v); }
}
function pluck(t0, m, g, pan) {
  const s0 = Math.floor(t0 * SR), f = mtof(m); let ph = 0;
  for (let i = 0; i < SR * 0.7; i++) { const t = i / SR; ph += f / SR;
    const v = (Math.sin(2 * Math.PI * ph) + 0.3 * Math.sin(2 * Math.PI * ph * 3) * Math.exp(-t * 12)) * Math.exp(-t * 6) * Math.min(1, t / 0.004) * g;
    add(s0 + i, v * (1 - pan), v * (1 + pan)); }
}
const bars = Math.ceil(DROP / BAR);
if (!BRIGHT) for (let b = 0; b < bars; b++) {   // lofi / warm
  const t = b * BAR, c = b % 4, end = Math.min(t + BAR, DROP), d0 = EARLY ? 0 : 1, d1 = EARLY ? 1 : 2, a0 = EARLY ? 1 : 3;
  if (end <= t) break;
  pad(t, end - t + 0.05, CH[c], 0.06);
  if (b >= d0) for (let k = 0; k < 4; k++) { const bt = t + k * BEAT; if (bt >= DROP) break;
    if (k === 0 || k === 2 || (k === 3 && b % 2 === 1)) bass(bt, Math.min(BEAT * (k === 0 ? 1.8 : 0.9), DROP - bt), ROOT[c], 0.16);
    if (k === 0 || (k === 2 && b >= d1)) kick(bt, 0.42);
    if (k === 2 && b >= d1 && b % 2 === 1) kick(bt + BEAT * 0.75, 0.3);
    if ((k === 1 || k === 3) && b >= d1) snap(bt, 0.22);
  }
  if (b >= d0) for (let e = 0; e < 8; e++) { const ht = t + e * BEAT / 2; if (ht >= DROP) break; hat(ht + (e % 2 ? 0.018 : 0), e % 2 ? 0.018 : 0.03, e % 2 ? 0.3 : -0.3); }
  if (b >= a0) { const arp = [0, 2, 1, 3, 2, 4, 3, 1]; arp.forEach((ix, e) => { const at = t + e * BEAT / 2; if (at < DROP) pluck(at, CH[c][ix] + 12, 0.035, (e % 2 ? 0.35 : -0.35)); }); }
}
else for (let b = 0; b < bars; b++) {   // lively / upbeat: groove from the first beat
  const t = b * BAR, c = b % 4, end = Math.min(t + BAR, DROP), UP = STYLE === "upbeat";
  if (end <= t) break;
  pad(t, end - t + 0.05, CH[c], 0.055);
  for (let k = 0; k < 4; k++) { const bt = t + k * BEAT; if (bt >= DROP) break;
    kick(bt, b === 0 && k === 0 ? 0.5 : 0.44);                                   // four on the floor
    if (k === 1 || k === 3) clap(bt, b === 0 ? 0.16 : 0.24);
    bass(bt + BEAT / 2, Math.min(BEAT * 0.45, DROP - bt - BEAT / 2), ROOT[c], 0.15);   // offbeat bass
    if (k === 0) bass(bt, Math.min(BEAT * 0.4, DROP - bt), ROOT[c], 0.12);
  }
  for (let e = 0; e < 16; e++) { const ht = t + e * BEAT / 4; if (ht >= DROP) break;
    hat(ht + (e % 2 ? 0.012 : 0), e % 4 === 2 ? (UP ? 0.05 : 0.04) : (e % 2 ? 0.014 : 0.024), e % 2 ? 0.3 : -0.3); }
  const arp = UP ? [0, 2, 4, 2, 1, 3, 4, 3, 0, 2, 4, 2, 1, 3, 4, 3] : [0, 2, 1, 3, 2, 4, 3, 1];
  const step = UP ? BEAT / 4 : BEAT / 2;
  arp.forEach((ix, e) => { const at = t + e * step; if (at < DROP) pluck(at, CH[c][ix] + 12, UP ? 0.03 : 0.036, (e % 2 ? 0.35 : -0.35)); });
}
// final hit: low boom + chord swell tail after the drop
{ const s0 = Math.floor(HIT * SR); let ph = 0;
  for (let i = 0; i < SR * 1.3 && s0 + i < N; i++) { const t = i / SR, f = 38 + 70 * Math.exp(-t * 14); ph += f / SR;
    const v = Math.sin(2 * Math.PI * ph) * Math.exp(-t * 2.4) * 0.6; add(s0 + i, v, v); } }
pad(HIT, DUR - HIT, CH[0], 0.03);
// soft reverse swell into the drums (bar 1)
{ const s0 = Math.floor((BAR - 0.8) * SR); let lp = 0;
  for (let i = 0; i < SR * 0.8; i++) { const t = i / SR, nz = rnd(); lp += (nz - lp) * 0.08; const v = lp * Math.pow(t / 0.8, 2) * 0.25; add(s0 + i, v, v); } }
// pad sidechain pump on the bright styles (ducks after every kick), then mix the pad in
{ const depth = STYLE === "upbeat" ? 0.6 : STYLE === "lively" ? 0.45 : 0;
  for (let i = 0; i < N; i++) { const t = i / SR, ph = (t % BEAT);
    const g = t < DROP ? 1 - depth * Math.exp(-ph * 9) : 1; L[i] += PL[i] * g; R[i] += PR[i] * g; } }
let peak = 0; for (let i = 0; i < N; i++) peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
const buf = Buffer.alloc(44 + N * 4);
buf.write("RIFF", 0); buf.writeUInt32LE(36 + N * 4, 4); buf.write("WAVEfmt ", 8); buf.writeUInt32LE(16, 16);
buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22); buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 4, 28);
buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34); buf.write("data", 36); buf.writeUInt32LE(N * 4, 40);
for (let i = 0; i < N; i++) { buf.writeInt16LE(Math.round(L[i] / peak * 0.89 * 32767), 44 + i * 4); buf.writeInt16LE(Math.round(R[i] / peak * 0.89 * 32767), 46 + i * 4); }
fs.writeFileSync(process.argv[2], buf);
console.log("peak", peak.toFixed(3), "bars", bars);
