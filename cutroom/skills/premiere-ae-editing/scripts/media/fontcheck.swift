// fontcheck: is a PostScript font name installed, and does it have the glyphs a string needs?
// usage: scripts/media/fontcheck [--text "≠→✓"] Name1 Name2 ...
// build once: swiftc -O scripts/media/fontcheck.swift -o scripts/media/fontcheck
// AE renders a missing glyph as BLANK with no error, and silently swaps a missing font: check before rendering.
// Core Text falls back to another font for unknown names, so "resolves to" differing from the asked name = NOT installed.
// Fonts only active through Adobe Fonts inside AE may not show here: confirm in AE with app.fonts.getFontsByPostScriptName.
import CoreText
import Foundation

var args = Array(CommandLine.arguments.dropFirst())
var text = "≠→←≈★✓✔×"
if let i = args.firstIndex(of: "--text"), i + 1 < args.count { text = args[i + 1]; args.removeSubrange(i...(i + 1)) }
for name in args {
    let f = CTFontCreateWithName(name as CFString, 40, nil)
    let real = CTFontCopyPostScriptName(f) as String
    var missing = ""
    for ch in text {
        var u = Array(String(ch).utf16)
        var g = [CGGlyph](repeating: 0, count: u.count)
        if !CTFontGetGlyphsForCharacters(f, &u, &g, u.count) { missing += String(ch) }
    }
    let installed = real == name || real.hasPrefix(name.split(separator: "-").first.map(String.init) ?? name)
    print("\(name): \(installed ? "installed" : "NOT INSTALLED") (resolves to \(real)); glyphs \(missing.isEmpty ? "all present" : "MISSING " + missing)")
}
