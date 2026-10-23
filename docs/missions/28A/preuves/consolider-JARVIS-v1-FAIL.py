# consolider.py
import argparse, hashlib, json, sys
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="Consolider preuves28A")
    p.add_argument("--comparative", required=True)
    p.add_argument("--corrected32", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--manifest", required=True)
    a = p.parse_args()

    data = {"mission": "28A", "model_count": 0, "scores": {}, "selected_model": "qwen3-coder-next:q4_K_M"}

    # comparative : 3 modèles, 6 cas
    c = json.loads(Path(a.comparative).read_text())
    for tag, summary in c["summary"].items():
        if tag not in data["scores"]:
            passed = sum(1 for case in c["cases"] if case["evaluation"]["pass"])
            total = len(c["cases"])
            data["scores"][tag] = {"passed": passed, "total": total}
    data["model_count"] = len(data["scores"])

    # corrected32 : 1 modèle, 6 cas
    c32 = json.loads(Path(a.corrected32).read_text())
    for tag, summary in c32["summary"].items():
        if tag not in data["scores"]:
            passed = sum(1 for case in c32["cases"] if case["evaluation"]["pass"])
            total = len(c32["cases"])
            data["scores"][tag] = {"passed": passed, "total": total}
            data["model_count"] += 1

    output_path = Path(a.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(data, indent=2, ensure_ascii=False)
    output_path.write_text(content, encoding="utf-8")

    manifest_path = Path(a.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
    manifest = {"sha256": sha}
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"{output_path} written with {data['model_count']} models")
    print(f"SHA256: {sha}")

if __name__ == "__main__":
    main()
