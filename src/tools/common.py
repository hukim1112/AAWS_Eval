import os

# --- 공통 설정 ---
ARTIFACT_DIR = os.path.join(os.getenv("PROJECT_ROOT", os.getcwd()), "artifacts", "code")
os.makedirs(ARTIFACT_DIR, exist_ok=True)
