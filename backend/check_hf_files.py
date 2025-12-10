"""
List files in Hugging Face repository to find correct model filename
"""

from huggingface_hub import list_repo_files

repo_id = "wellCh4n/tomato-leaf-disease-classification-resnet50"

print(f"📂 Files in {repo_id}:")
print("=" * 70)

try:
    files = list_repo_files(repo_id)
    for f in files:
        print(f"   {f}")
except Exception as e:
    print(f"Error: {e}")
