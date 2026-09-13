// Generic local webfont loader for Remotion.
//
// Why this exists: Remotion renders in headless Chromium, which only has a
// handful of system fonts. The pipeline hardcodes Latin fonts (Space Grotesk /
// Inter), so any non-Latin script (Devanagari, CJK, Arabic, etc.) silently
// renders blank — a serious, invisible failure.
//
// This helper injects an @font-face for a font file placed in `public/` so it
// is bundled and available to the headless renderer. Pair with a theme whose
// headingFont/bodyFont names the bundled family.

export interface LocalFont {
  /** Font-family name used in CSS (e.g. "Shobhika"). */
  family: string;
  /** Single font file path (relative to public/) OR array of sources (woff2/ttf). */
  url?: string;
  src?: string | string[];
  /** Format hint for the @font-face src (used when url is a single string). */
  format?: "truetype" | "opentype" | "woff2";
  /** Weight range, e.g. "400 700". */
  weight?: string;
}

export function localFontFaceCss(font: LocalFont): string {
  const format = font.format ?? "truetype";
  const weight = font.weight ?? "400 700";
  let src: string;
  if (typeof font.src === "string") {
    src = `url('${font.src}') format('${format}')`;
  } else if (Array.isArray(font.src)) {
    src = font.src
      .map((s) => `url('${s}') format('${s.split(".").pop()}')`)
      .join(", ");
  } else if (font.url) {
    src = `url('${font.url}') format('${format}')`;
  } else {
    src = "";
  }
  return `
    @font-face {
      font-family: '${font.family}';
      src: ${src};
      font-weight: ${weight};
      font-display: swap;
    }
  `;
}

/**
 * Inject one or more local @font-face rules into the document head.
 * Safe to call once per render (idempotent by family name).
 */
export function injectLocalFonts(fonts: LocalFont[]): void {
  if (typeof document === "undefined") return;
  for (const font of fonts) {
    const id = `local-font-${font.family}`;
    if (document.getElementById(id)) continue;
    const style = document.createElement("style");
    style.id = id;
    style.innerHTML = localFontFaceCss(font);
    document.head.appendChild(style);
  }
}
