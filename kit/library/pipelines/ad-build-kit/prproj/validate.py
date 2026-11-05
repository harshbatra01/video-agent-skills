import sys, re, collections, gzip, difflib
import xml.etree.ElementTree as ET
def validate(orig_xml, new_prproj):
    new_txt=gzip.open(new_prproj,'rb').read().decode('utf-8')
    old_txt=open(orig_xml,encoding='utf-8').read()
    root=ET.fromstring(new_txt)                       # 1. well-formed
    ids=collections.Counter(e.attrib['ObjectID'] for e in root if 'ObjectID' in e.attrib)
    uids=collections.Counter(e.attrib['ObjectUID'] for e in root if 'ObjectUID' in e.attrib)
    dup=[k for k,v in ids.items() if v>1]+[k for k,v in uids.items() if v>1]
    print('objects', len(root), '| duplicate ids:', dup)
    bad=[]; nref=0
    for e in root.iter():
        if 'ObjectRef' in e.attrib:
            nref+=1
            if e.attrib['ObjectRef'] not in ids: bad.append(('ref',e.attrib['ObjectRef']))
        if 'ObjectURef' in e.attrib:
            nref+=1
            if e.attrib['ObjectURef'] not in uids: bad.append(('uref',e.attrib['ObjectURef']))
    print('references', nref, '| unresolved:', bad[:10], len(bad))
    # binary hashes: every referenced hash must have inline data somewhere, before first use
    seen=set(); missing=set()
    for m in re.finditer(r'BinaryHash="([^"]+)"(/?)>', new_txt):
        h=m.group(1); has_data=(m.group(2)=='' and not new_txt.startswith('</',m.end()) )
        if has_data: seen.add(h)
        elif h not in seen: missing.add(h)
    print('blob hashes referenced before their data:', len(missing), list(missing)[:3])
    # textual diff summary of the original region (everything before appended objects)
    old_lines=old_txt.split('\n'); new_lines=new_txt.split('\n')
    sm=difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
    ops=[op for op in sm.get_opcodes() if op[0]!='equal']
    print('changed regions:', len(ops))
    for tag,i1,i2,j1,j2 in ops:
        ctx=old_lines[i1-1][:70] if i1>0 else ''
        print(' %-7s old %d-%d new %d-%d (%d->%d lines) after: %s'%(tag,i1,i2,j1,j2,i2-i1,j2-j1,ctx.strip()))
    return root
if __name__=='__main__': validate(sys.argv[1], sys.argv[2])
