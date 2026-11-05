// Person cut-out mask with Apple's Vision framework through JavaScript for Automation (no compiler, no installs).
// Usage: osascript -l JavaScript person_mask.js <in.jpg> <out_mask.png>   -> white = person, black = background.
ObjC.import('Foundation'); ObjC.import('Vision'); ObjC.import('CoreImage'); ObjC.import('AppKit');
function run(argv) {
  const url = $.NSURL.fileURLWithPath(argv[0]);
  const img = $.CIImage.imageWithContentsOfURL(url);
  if (img.isNil()) return 'cannot read ' + argv[0];
  const req = $.VNGeneratePersonSegmentationRequest.alloc.init;
  req.qualityLevel = 0;                       // 0 = accurate
  req.outputPixelFormat = 1278226488;         // kCVPixelFormatType_OneComponent8 ('L008')
  const handler = $.VNImageRequestHandler.alloc.initWithCIImageOptions(img, $({}));
  const err = Ref();
  if (!handler.performRequestsError($([req]), err)) return 'vision failed';
  const res = req.results;
  if (res.count == 0) return 'no person found';
  let mask = $.CIImage.imageWithCVPixelBuffer(res.objectAtIndex(0).pixelBuffer);
  const ext = img.extent, mext = mask.extent;
  mask = mask.imageByApplyingTransform($.CGAffineTransformMakeScale(ext.size.width / mext.size.width, ext.size.height / mext.size.height));
  const ctx = $.CIContext.context;
  const cg = ctx.createCGImageFromRect(mask, ext);
  const rep = $.NSBitmapImageRep.alloc.initWithCGImage(cg);
  const data = rep.representationUsingTypeProperties($.NSBitmapImageFileTypePNG, $({}));
  data.writeToFileAtomically(argv[1], true);
  return 'mask written ' + ext.size.width + 'x' + ext.size.height;
}
