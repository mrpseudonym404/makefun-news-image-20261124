// Entry for make.fun bounty news-image-20261124: "Sum up 24 November's world
// news in one image". The program copies the infographic this repository holds
// (entry-20261124.png, 1024x1024, built with build_image_20261124.py) to
// /output/entry.png — the one image the bounty asks the program to write.
// Deterministic: the same input bytes are copied on every run.
// Node 22 stdlib only.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry-20261124.png");
const outDir = "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
