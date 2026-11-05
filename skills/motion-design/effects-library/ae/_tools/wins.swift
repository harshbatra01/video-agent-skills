// macOS only: lists After Effects windows (id, owner, title, size, ONSCREEN) for effects_build.py's dialog check.
// Build: swiftc -O wins.swift -o wins   (Windows has no equivalent here: effects_build.py skips dialog handling there)
import Cocoa
let opts = CGWindowListOption(arrayLiteral: .optionAll)
if let list = CGWindowListCopyWindowInfo(opts, kCGNullWindowID) as? [[String: Any]] {
  for w in list {
    let owner = w[kCGWindowOwnerName as String] as? String ?? ""
    if owner.contains("After Effects") {
      let name = w[kCGWindowName as String] as? String ?? ""
      let num = w[kCGWindowNumber as String] as? Int ?? 0
      let b = w[kCGWindowBounds as String] as? [String: Any] ?? [:]
      let on = w[kCGWindowIsOnscreen as String] as? Bool ?? false
      print(num, owner, "|", name, "|", b["Width"] ?? 0, "x", b["Height"] ?? 0, on ? "ONSCREEN" : "")
    }
  }
}
