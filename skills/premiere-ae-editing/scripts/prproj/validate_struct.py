"""Structure checks: well-formed, unique ids, references resolve (vs source), blob data before use, no new orphans, media files exist."""
import sys, re, gzip, collections, os
import xml.etree.ElementTree as ET


def load(p):
    return gzip.open(p, 'rb').read().decode('utf-8') if p.endswith('.prproj') else open(p, encoding='utf-8').read()


def analyse(txt):
    root = ET.fromstring(txt)
    ids = collections.Counter(e.attrib['ObjectID'] for e in root if 'ObjectID' in e.attrib)
    uids = collections.Counter(e.attrib['ObjectUID'] for e in root if 'ObjectUID' in e.attrib)
    dup = [k for k, v in ids.items() if v > 1] + [k for k, v in uids.items() if v > 1]
    unresolved = set()
    for e in root.iter():
        if 'ObjectRef' in e.attrib and e.attrib['ObjectRef'] not in ids: unresolved.add(('ref', e.attrib['ObjectRef']))
        if 'ObjectURef' in e.attrib and e.attrib['ObjectURef'] not in uids: unresolved.add(('uref', e.attrib['ObjectURef']))
    seen, before = set(), set()
    for m in re.finditer(r'BinaryHash="([^"]+)"(/?)>', txt):
        h = m.group(1)
        if m.group(2) == '' and not txt.startswith('</', m.end()): seen.add(h)
        elif h not in seen: before.add(h)
    # reachability from the Project object
    by = {}
    for e in root:
        k = e.attrib.get('ObjectID') or e.attrib.get('ObjectUID')
        if k: by[k] = e
    start = [e for e in root if e.tag == 'Project' and 'ObjectID' in e.attrib][0]
    todo = [start]; reach = set()
    while todo:
        e = todo.pop()
        k = e.attrib.get('ObjectID') or e.attrib.get('ObjectUID')
        if k in reach: continue
        reach.add(k)
        for sub in e.iter():
            r = sub.attrib.get('ObjectRef') or sub.attrib.get('ObjectURef')
            if r and r in by and r not in reach: todo.append(by[r])
    orphans = collections.Counter(by[k].tag for k in by if k not in reach)
    media = [(e.findtext('FilePath') or '') for e in root if e.tag == 'Media']
    return dict(n=len(root), dup=dup, unresolved=unresolved, blob_before=before, orphans=orphans, media=media)


a = analyse(load(sys.argv[1])); b = analyse(load(sys.argv[2]))
print('objects %d -> %d' % (a['n'], b['n']))
print('duplicate ids:', b['dup'])
print('unresolved refs new:', sorted(b['unresolved'] - a['unresolved']), '| already in source:', sorted(a['unresolved']))
print('blob hashes used before their data:', len(b['blob_before']))
print('orphan objects source:', dict(a['orphans']))
print('orphan objects new   :', dict(b['orphans']))
new_media = [m for m in b['media'] if m not in a['media']]
print('new media objects: %d, all files exist: %s' % (len(new_media), all(os.path.exists(m) for m in new_media)))
for m in new_media: print('   ', os.path.basename(m))
