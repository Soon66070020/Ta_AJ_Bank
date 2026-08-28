import sys
sys.stdout.reconfigure(encoding='utf-8')
import nbformat
from nbclient import NotebookClient

nb_path = r'e:\DGA_ALL\DGA_3\group_6\mso_culture_goal_analysis.ipynb'
print(f"Reading {nb_path}...")
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

client = NotebookClient(nb, timeout=600, kernel_name='python3', resources={'metadata': {'path': r'e:\DGA_ALL\DGA_3\group_6'}})
print("Executing notebook cells...")
client.execute()

print("Writing executed notebook back to disk...")
with open(nb_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("🎉 Execution completed successfully! All cells executed without error.")
