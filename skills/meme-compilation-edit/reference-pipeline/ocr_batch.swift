// macOS only (Apple Vision). Build: swiftc -O ocr_batch.swift -o ocr_batch
// ocr_batch <file>... : prints one JSON object per line with line and word boxes (+ "q" outlines that follow slanted text)
// Boxes are normalized to the image, origin top-left: [x0, y0, x1, y1]
import Vision
import AppKit
import Foundation

func pt(_ p: CGPoint) -> [Double] {
    return [Double(p.x), Double(1 - p.y)].map { ($0 * 10000).rounded() / 10000 }
}
// the text's own outline (follows slanted text on signs and photos): TL, TR, BR, BL, origin top-left
func quad(_ o: VNRectangleObservation) -> [[Double]] {
    return [pt(o.topLeft), pt(o.topRight), pt(o.bottomRight), pt(o.bottomLeft)]
}

func box(_ r: CGRect) -> [Double] {
    return [Double(r.minX), Double(1 - r.maxY), Double(r.maxX), Double(1 - r.minY)].map { ($0 * 10000).rounded() / 10000 }
}

for path in CommandLine.arguments.dropFirst() {
    var out: [String: Any] = ["file": path]
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        out["error"] = "load"
        print(String(data: try! JSONSerialization.data(withJSONObject: out), encoding: .utf8)!)
        continue
    }
    out["w"] = cg.width
    out["h"] = cg.height
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    var lines: [[String: Any]] = []
    for obs in req.results ?? [] {
        guard let cand = obs.topCandidates(1).first else { continue }
        var words: [[String: Any]] = []
        var idx = cand.string.startIndex
        for w in cand.string.split(separator: " ") {
            if let r = cand.string.range(of: w, range: idx..<cand.string.endIndex) {
                if let wb = try? cand.boundingBox(for: r) {
                    words.append(["t": String(w), "b": box(wb.boundingBox), "q": quad(wb)])
                }
                idx = r.upperBound
            }
        }
        lines.append(["t": cand.string, "b": box(obs.boundingBox), "q": quad(obs), "c": Double(cand.confidence), "words": words])
    }
    out["lines"] = lines
    print(String(data: try! JSONSerialization.data(withJSONObject: out), encoding: .utf8)!)
    fflush(stdout)
}
