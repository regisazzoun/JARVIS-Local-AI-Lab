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
    cases_list = c.get("cases", [])
    
    # Compter les cas par modèle en respectant case.model
    for case in cases_list:
        tag = case.get("model")
        if tag:
            passed = 1 if case.get("evaluation", {}).get("pass") is True else 0
            if tag not in data["scores"]:
                data["scores"][tag] = {"passed": 0, "total": 0}
            data["scores"][tag]["passed"] += passed
            data["scores"][tag]["total"] += 1
    
    data["model_count"] = len(data["scores"])

    # corrected32 : 1 modèle, 6 cas
    c32 = json.loads(Path(a.corrected32).read_text())
    cases_list32 = c32.get("cases", [])
    
    for case in cases_list32:
        tag = case.get("model")
        if tag:
            passed = 1 if case.get("evaluation", {}).get("pass") is True else 0
            if tag not in data["scores"]:
                data["scores"][tag] = {"passed": 0, "total": 0}
            data["scores"][tag]["passed"] += passed
            data["scores"][tag]["total"] += 1

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
