// macOS Vision OCR: prints one line per recognised text block as "y_center<TAB>x_center<TAB>text" (normalised coords, y from top).
import Foundation
import Vision
import AppKit
let path = CommandLine.arguments[1]
guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { fputs("cannot load \(path)\n", stderr); exit(1) }
let req = VNRecognizeTextRequest { r, _ in
    for o in (r.results as? [VNRecognizedTextObservation]) ?? [] {
        guard let t = o.topCandidates(1).first else { continue }
        let b = o.boundingBox
        print(String(format: "%.4f\t%.4f\t%@", 1 - (b.midY), b.midX, t.string))
    }
}
req.recognitionLevel = .accurate; req.usesLanguageCorrection = false
try VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
