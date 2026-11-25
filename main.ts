// Entry harness for the news-image-20261124 entry.
//
// Copies the pre-built entry image (entry-20261124.png, rendered by
// build_image_20261124.py) to the harness output directory as entry.png.
// Node 22 standard library only; no dependencies, no network.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
const src = join(here, "entry-20261124.png");
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);
console.log(`entry.png written to ${outDir}`);
