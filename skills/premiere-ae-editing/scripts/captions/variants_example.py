def bx(S, pad=18, op=68.0):
    S.f[17] = color(140, 17, 28); S.f[18] = u8(1); S.f[19] = f32(op); S.f[20] = f32(pad); S.f[11] = u8(0)
def mk(font, off=None):
    def f(T):
        S = base(T, font=font); bx(S)
        if off is not None: S.f[33] = ("table", Table({2: f32(off)}))
    return f
APPLY = {0: mk("LoraItalic-Italic"), 1: mk("LoraItalic-MediumItalic"), 2: mk("Lora-Italic"), 3: mk("DMSerifDisplay-Italic"),
         4: mk("Georgia-Italic"), 5: mk("LoraItalic-Italic", -0.439), 6: mk("LoraItalic-Italic", -0.259), 7: mk("Lora Italic")}
