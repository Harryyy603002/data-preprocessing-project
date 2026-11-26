"""Báo lỗi nếu notebook chưa chạy/có lỗi hoặc còn placeholder."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK = ROOT / "book"
MARKERS = ("[điền", "[Chèn", "[HỌ VÀ TÊN", "[MSSV", "[LỚP",
           "cần hoàn thiện", "cần điền")
problems = []

for path in sorted(BOOK.glob("*.ipynb")):
    nb = json.loads(path.read_text(encoding="utf8"))
    code = [c for c in nb["cells"]
            if c["cell_type"] == "code" and "".join(c["source"]).strip()]
    for i, c in enumerate(code):
        if c.get("execution_count") is None:
            problems.append(f"{path.name}: ô code #{i} chưa chạy")
        if any(o.get("output_type") == "error" for o in c.get("outputs", [])):
            problems.append(f"{path.name}: ô code #{i} có lỗi")
    for c in nb["cells"]:
        if c["cell_type"] == "markdown":
            text = "".join(c["source"])
            problems += [f"{path.name}: còn '{m}'" for m in MARKERS if m in text]

for path in [ROOT / "README.md", BOOK / "_config.yml", *BOOK.glob("*.md")]:
    text = path.read_text(encoding="utf8")
    problems += [f"{path.name}: còn '{m}'" for m in MARKERS if m in text]

if problems:
    print("\n".join(problems))
    sys.exit(1)
print("OK: notebook đã chạy sạch, không còn placeholder.")
