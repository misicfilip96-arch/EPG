#!/usr/bin/env python3
import gzip
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

# Priority order for duplicate XMLTV channel IDs.
SOURCES = [
    ("RS1", "https://epgshare01.online/epgshare01/epg_ripper_RS1.xml.gz"),
    ("SPORTKLUB1", "https://epgshare01.online/epgshare01/epg_ripper_SPORTKLUB1.xml.gz"),
    ("BA1", "https://epgshare01.online/epgshare01/epg_ripper_BA1.xml.gz"),
    ("HR1", "https://epgshare01.online/epgshare01/epg_ripper_HR1.xml.gz"),
]

OUT_GZ = Path("epg.xml.gz")
STATUS = Path("status.txt")
UA = "Mozilla/5.0 XMLTV-Merger/1.0"

def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def clone(el):
    return ET.fromstring(ET.tostring(el, encoding="utf-8"))

def main():
    feeds = []
    owner = {}
    channel_elements = {}
    status = []

    for priority, (name, url) in enumerate(SOURCES):
        print(f"Downloading {name}...")
        raw = download(url)
        xml = gzip.decompress(raw)
        root = ET.fromstring(xml)
        channels = list(root.findall("channel"))
        programmes = list(root.findall("programme"))
        feeds.append((priority, name, channels, programmes))

        claimed = 0
        for ch in channels:
            cid = (ch.get("id") or "").strip()
            if cid and cid not in owner:
                owner[cid] = priority
                channel_elements[cid] = clone(ch)
                claimed += 1

        status.append(
            f"{name}: {len(channels)} channels, {len(programmes)} programmes, "
            f"{claimed} unique channel IDs kept"
        )

    tv = ET.Element("tv", {
        "generator-info-name": "RS1+SPORTKLUB1+BA1+HR1 merger",
        "generator-info-url": "https://epgshare01.online/"
    })

    for cid in owner:
        tv.append(channel_elements[cid])

    seen_programmes = set()
    kept_programmes = 0

    for priority, name, channels, programmes in feeds:
        for p in programmes:
            cid = (p.get("channel") or "").strip()
            if not cid or owner.get(cid) != priority:
                continue

            title = p.find("title")
            key = (
                cid,
                p.get("start", ""),
                p.get("stop", ""),
                title.text if title is not None else ""
            )
            if key in seen_programmes:
                continue
            seen_programmes.add(key)
            tv.append(clone(p))
            kept_programmes += 1

    xml_bytes = ET.tostring(tv, encoding="utf-8", xml_declaration=True)
    with gzip.open(OUT_GZ, "wb", compresslevel=9) as f:
        f.write(xml_bytes)

    status += [
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        f"Unique channel IDs: {len(owner)}",
        f"Programmes kept: {kept_programmes}",
        "Duplicate-ID priority: RS1 > SPORTKLUB1 > BA1 > HR1",
    ]
    STATUS.write_text("\n".join(status), encoding="utf-8")
    print("\n".join(status))

if __name__ == "__main__":
    main()
