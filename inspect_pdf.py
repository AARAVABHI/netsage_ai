from pathlib import Path
p = Path(r'c:\Users\aarav\Desktop\netsage_ai\NetSage AI Technical Documentation.pdf')
print('exists:', p.exists())
print('size:', p.stat().st_size if p.exists() else 'missing')
try:
    from pypdf import PdfReader
    reader = PdfReader(str(p))
    print('pages:', len(reader.pages))
    for i, page in enumerate(reader.pages[:8], start=1):
        text = page.extract_text() or ''
        print('--- PAGE', i, '---')
        print(text[:3000])
except Exception as e:
    import traceback; traceback.print_exc()
