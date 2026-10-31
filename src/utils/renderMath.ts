import katex from 'katex';

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/**
 * Renders a plain/markdown-lite string containing $...$ (inline math)
 * and $$...$$ (display math) into safe HTML with server-rendered KaTeX.
 * Uses output: 'html' to avoid duplicate MathML trees and keep static HTML lightweight.
 */
export function renderMathText(input: string, multiline = false): string {
  if (!input) return '';

  const mathBlocks: string[] = [];
  const placeholder = (idx: number) => `@@MATH_BLOCK_${idx}@@`;

  // 1. Extract display math $$...$$
  let processed = input.replace(/\$\$([\s\S]+?)\$\$/g, (_match, tex) => {
    try {
      const html = katex.renderToString(tex.trim(), {
        displayMode: true,
        output: 'html',
        throwOnError: false,
        strict: false,
      });
      mathBlocks.push(`<div class="katex-block" style="overflow-x:auto; margin:0.45rem 0; padding:0.2rem 0;">${html}</div>`);
    } catch {
      mathBlocks.push(`<code>${escapeHtml(tex)}</code>`);
    }
    return placeholder(mathBlocks.length - 1);
  });

  // 2. Extract inline math $...$
  processed = processed.replace(/\$([^\$\n]+?)\$/g, (_match, tex) => {
    try {
      const html = katex.renderToString(tex.trim(), {
        displayMode: false,
        output: 'html',
        throwOnError: false,
        strict: false,
      });
      mathBlocks.push(html);
    } catch {
      mathBlocks.push(`<code>${escapeHtml(tex)}</code>`);
    }
    return placeholder(mathBlocks.length - 1);
  });

  // 3. Escape remaining HTML
  processed = escapeHtml(processed);

  // 4. Render **bold**
  processed = processed.replace(/\*\*([^*]+?)\*\*/g, '<strong style="color: var(--text-primary);">$1</strong>');

  // 5. Handle newlines if multiline
  if (multiline) {
    processed = processed
      .split(/\n{2,}/)
      .map((para) => `<p style="margin: 0 0 0.55rem 0; line-height: 1.65;">${para.replace(/\n/g, '<br/>')}</p>`)
      .join('');
  }

  // 6. Restore math blocks
  processed = processed.replace(/@@MATH_BLOCK_(\d+)@@/g, (_m, idx) => mathBlocks[Number(idx)] || '');

  return processed;
}
