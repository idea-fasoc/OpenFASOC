"""
More robust JSON parser for training data with escape sequence issues.
"""

import json
import re
import glob
from pathlib import Path


def fix_json_content(content: str) -> str:
    #remove any trailing commas before closing braces/brackets
    content = re.sub(r',(\s*[}\]])', r'\1', content)
    
    #fix escaped quotes in strings
    content = content.replace('\\"', '"')
    
    #replace single quotes with double quotes for keys/strings (simple heuristic)
    content = re.sub(r"'([^']*)'", r'"\1"', content)
    
    return content

#slightly changed, removed an unnecessary clause. check to see if still functional as expected
def extract_and_fix_json_from_markdown(file_path: str) -> list:
    data = []
    
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    json_blocks = re.findall(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
    
    for block in json_blocks:
        try:
            parsed = json.loads(block)
            data.append(parsed)
        except json.JSONDecodeError as e:
            print(f"Direct parse failed for {file_path}: {e}")
            
            try:
                fixed_block = fix_json_content(block)
                parsed = json.loads(fixed_block)
                data.append(parsed)
            except json.JSONDecodeError as e2:
                print(f"Fixed parse failed for {file_path}: {e2}")
                
                filename_match = re.search(r'"filename":\s*"([^"]*)"', block)
                filename = filename_match.group(1) if filename_match else ""
                
                analysis_match = re.search(r'"analysis":\s*\[(.*?)\]', block, re.DOTALL)
                analysis = []
                if analysis_match:
                    analysis_content = analysis_match.group(1)
                    issue_matches = re.findall(r'"issue":\s*"([^"]*)"', analysis_content)
                    for issue in issue_matches:
                        analysis.append({
                            "issue": issue,
                            "explanation": {
                                "problem": "Extracted issue",
                                "reason": "JSON parsing issue",
                                "fix": "Manual extraction"
                            }
                        })
                    
                fixed_code_match = re.search(r'"fixed_code":\s*"(.*)"$', block, re.DOTALL | re.MULTILINE)
                if fixed_code_match:
                    fixed_code = fixed_code_match.group(1)
                    try:
                        fixed_code = fixed_code.encode("utf-8", "ignore").decode("unicode_escape", "ignore")
                    except:
                        #fallback to basic replacement if encoding fails
                        fixed_code = fixed_code.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
                else:
                    fixed_code = ""
    
    return data


def main():
    print("Using robust JSON parser for problematic files...")
    
    repo_root = Path(__file__).resolve().parent.parent.parent
    
    files_7b = glob.glob(str(repo_root / "dataset_for_sft/prediction_finetuned/7b-ft/*.txt"))
    all_data_7b = []
    
    for file_path in files_7b:
        print(f"   • {Path(file_path).name}")
        data = extract_and_fix_json_from_markdown(file_path)
        all_data_7b.extend(data)
    
    files_13b = glob.glob(str(repo_root / "dataset_for_sft/prediction_finetuned/13b-ft/*.txt"))
    all_data_13b = []
    
    for file_path in files_13b:
        print(f"   • {Path(file_path).name}")
        data = extract_and_fix_json_from_markdown(file_path)
        all_data_13b.extend(data)
    
    output_dir = Path(".")
    output_dir.mkdir(exist_ok=True)
    
    output_7b = output_dir / "train_data_7b_robust.jsonl"
    with open(output_7b, 'w', encoding='utf-8') as f:
        for item in all_data_7b:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    output_13b = output_dir / "train_data_13b_robust.jsonl"
    with open(output_13b, 'w', encoding='utf-8') as f:
        for item in all_data_13b:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"7B model: {len(all_data_7b)} samples -> {output_7b}")
    print(f"13B model: {len(all_data_13b)} samples -> {output_13b}")
    print(f"Total samples: {len(all_data_7b) + len(all_data_13b)}")


if __name__ == "__main__":
    main() 