// macOS only: lists Premiere windows (pid, id, layer, on-screen, size, title). Build: swiftc -O wins.swift -o wins
import CoreGraphics
import Foundation
let opts = CGWindowListOption(arrayLiteral: .optionAll)
if let list = CGWindowListCopyWindowInfo(opts, kCGNullWindowID) as? [[String: Any]] {
    for w in list {
        let owner = w[kCGWindowOwnerName as String] as? String ?? ""
        if owner.contains("Premiere") {
            let pid = w[kCGWindowOwnerPID as String] as? Int ?? 0
            let num = w[kCGWindowNumber as String] as? Int ?? 0
            let name = w[kCGWindowName as String] as? String ?? ""
            let b = w[kCGWindowBounds as String] as? [String: Any] ?? [:]
            let layer = w[kCGWindowLayer as String] as? Int ?? 0
            let onscreen = w[kCGWindowIsOnscreen as String] as? Bool ?? false
            print("\(pid) \(num) layer=\(layer) on=\(onscreen) \(Int(b["Width"] as? Double ?? 0))x\(Int(b["Height"] as? Double ?? 0)) '\(name)'")
        }
    }
}
