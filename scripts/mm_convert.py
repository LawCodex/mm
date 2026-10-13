#!/usr/bin/env python3
"""Convert the 2008 Constitution of the Republic of the Union of Myanmar (bilingual print of the
Ministry of Information, as published on the Pyidaungsu Hluttaw website and preserved by the
Internet Archive) to Markdown.

The PDF alternates English and Myanmar pages. The Myanmar pages use a legacy non-Unicode font
(Win* fonts: the extracted text is Latin gibberish such as "zGJUpnf;ykHtajccHOya'"), so only the
English pages are converted.

Usage: mm_convert.py PDF OUT_MD
"""
import re
import subprocess
import sys
from datetime import date

PDF, OUT = sys.argv[1], sys.argv[2]
SRC = ("https://web.archive.org/web/20170622204415/"
       "http://pyidaungsu.hluttaw.mm/uploads/pdf/constitution-2008.pdf")
EN_WORDS = re.compile(r"\b(the|of|and|shall|to|in|or|be|Union|State)\b")


def english(page):
    words = re.findall(r"[A-Za-z]+", page)
    if len(words) < 3:
        return False
    return len(EN_WORDS.findall(page)) / len(words) > 0.12 or page.strip().startswith(("Chapter", "Schedule"))


def main():
    txt = subprocess.run(["pdftotext", "-enc", "UTF-8", PDF, "-"], capture_output=True).stdout.decode()
    pages = txt.split("\f")
    start = next(i for i, p in enumerate(pages) if p.strip().startswith("Preamble"))
    lines = []
    for p in pages[start:]:
        if not english(p):
            continue
        ls = [x.strip() for x in p.split("\n") if x.strip()]
        if ls and re.fullmatch(r"\d{1,3}", ls[0]):
            ls = ls[1:]  # page number
        if ls and re.fullmatch(r"\d{1,3}", ls[-1]):
            ls = ls[:-1]
        lines += ls
    out, buf, last = [], [], 0
    cur_chap = None
    cur_title = ""
    newpara = re.compile(r"^(\([a-z]{1,4}\)|\(\d+\)|\([ivx]+\))(\s|$)")

    def flush():
        para = ""
        for ln in buf:
            if not para:
                para = ln
            elif newpara.match(ln) or (re.match(r"^[A-Z]", ln) and para.endswith((".", ";", ":"))):
                out.append(para)
                para = ln
            elif newpara.fullmatch(para):
                para += " " + ln
            else:
                para += " " + ln
        if para:
            out.append(para)
        buf.clear()
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln == "Preamble":
            flush()
            out.append("## Preamble")
        elif re.fullmatch(r"Chapter [IVXL]+", ln) and ln == cur_chap:
            # the chapter heading is printed twice (divider page + first page of the chapter)
            i += 1
            while i < len(lines) and not re.match(r"^\d+\.", lines[i]) and len(lines[i]) < 70 \
                    and not lines[i].endswith((".", ";", ":")):
                if lines[i].lower() not in cur_title.lower():
                    buf.append(lines[i])  # keep sub-headings that follow the repeated title
                i += 1
            continue
        elif re.fullmatch(r"Chapter [IVXL]+", ln):
            flush()
            cur_chap = ln
            cur_title = ""
            title = lines[i + 1] if i + 1 < len(lines) else ""
            j = i + 2
            while j < len(lines) and not re.match(r"^\d+\.", lines[j]) and lines[j][:1].isupper() \
                    and not lines[j].endswith(".") and len(title) < 120 and lines[j].istitle() and not re.fullmatch(r"Chapter [IVXL]+", lines[j]):
                title += " " + lines[j]
                j += 1
            out.append(f"## {ln} — {title}")
            cur_title = title
            i = j
            if i < len(lines) and lines[i] == ln:
                continue
            continue
        elif re.fullmatch(r"Schedule (One|Two|Three|Four|Five)", ln, re.I):
            flush()
            out.append(f"## {ln}")
            last = 10 ** 6
        else:
            m = re.match(r"^(\d{1,3})\.\s*(.*)$", ln)
            if m and last < int(m.group(1)) <= last + 3:
                flush()
                last = int(m.group(1))
                out.append(f"### Section {last}")
                if m.group(2):
                    buf.append(m.group(2))
            else:
                # section numbers printed alone on a line ("12.") followed by the text
                buf.append(ln)
        i += 1
    flush()
    body = "\n\n".join(re.sub(r"^(\d+[.)]\s|[#>*+|]|-\s)", r"\\\1", x) if not x.startswith("#") else x
                       for x in out)
    fm = f"""---
title: "Constitution of the Republic of the Union of Myanmar (2008)"
identifier: "Constitution 2008"
type: constitution
jurisdiction: mm
language: en
date: 2008-09-01
status: unknown
status_note: "Status contested since 1 February 2021 — see README"
translation: true
source: "{SRC}"
retrieved: {date.today().isoformat()}
---

# Constitution of the Republic of the Union of Myanmar (2008)

"""
    open(OUT, "w", encoding="utf-8", newline="\n").write(fm + body + "\n")


if __name__ == "__main__":
    main()
