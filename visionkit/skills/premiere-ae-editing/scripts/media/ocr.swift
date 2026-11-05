// ocr: Apple Vision OCR (macOS replacement for the Windows ocr.ps1), same JSON shape so ocrfind.py works unchanged.
// usage: scripts/media/ocr out.json img1.png img2.png ...
// build once (CommandLineTools swiftc): swiftc -O scripts/media/ocr.swift -o scripts/media/ocr
// out.json = {"img1.png": [{"text": "line text", "words": [["word", x, y, w, h], ...]}, ...], ...}
// Boxes are image pixels, origin top-left (Vision's normalized bottom-left boxes converted).
import Vision
import AppKit
import Foundation

let args = Array(CommandLine.arguments.dropFirst())
guard args.count >= 2 else {
    FileHandle.standardError.write("usage: ocr out.json img1.png [img2.png ...]\n".data(using: .utf8)!)
    exit(2)
}
let outPath = args[0]
var all: [String: Any] = [:]

func rect(_ r: CGRect, _ w: Double, _ h: Double) -> [Double] {
    let x = Double(r.minX) * w, y = (1 - Double(r.maxY)) * h
    return [x, y, Double(r.width) * w, Double(r.height) * h].map { ($0 * 10).rounded() / 10 }
}

for path in args.dropFirst() {
    let name = (path as NSString).lastPathComponent
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        FileHandle.standardError.write("could not load \(path)\n".data(using: .utf8)!)
        all[name] = []
        continue
    }
    let W = Double(cg.width), H = Double(cg.height)
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    var lines: [[String: Any]] = []
    for obs in req.results ?? [] {
        guard let cand = obs.topCandidates(1).first else { continue }
        var words: [[Any]] = []
        var idx = cand.string.startIndex
        for w in cand.string.split(separator: " ") {
            guard let r = cand.string.range(of: w, range: idx..<cand.string.endIndex) else { continue }
            if let wb = try? cand.boundingBox(for: r) {
                words.append([String(w)] + rect(wb.boundingBox, W, H))
            }
            idx = r.upperBound
        }
        lines.append(["text": cand.string, "words": words])
    }
    // Vision returns lines roughly top to bottom; sort to be sure (by y then x of the first word)
    lines.sort { a, b in
        let wa = (a["words"] as? [[Any]])?.first, wb = (b["words"] as? [[Any]])?.first
        let ya = (wa?[2] as? Double) ?? 0, yb = (wb?[2] as? Double) ?? 0
        if abs(ya - yb) > 4 { return ya < yb }
        return ((wa?[1] as? Double) ?? 0) < ((wb?[1] as? Double) ?? 0)
    }
    all[name] = lines
}
let data = try! JSONSerialization.data(withJSONObject: all, options: [])
FileManager.default.createFile(atPath: outPath, contents: data)
print("ocr: \(args.count - 1) image(s) -> \(outPath)")
