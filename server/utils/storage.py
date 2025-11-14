import os
from werkzeug.utils import secure_filename

BASE_SKIN_DIR = os.path.join(os.path.dirname(__file__), '..', 'resources', 'skin')

ALLOWED_EXTS = {'.png', '.jpg', '.jpeg'}

def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def _ext_from_filename(filename: str):
    filename = secure_filename(filename)
    _, ext = os.path.splitext(filename.lower())
    return ext if ext in ALLOWED_EXTS else None

def _build_public_url(category: str, cfg_id: int, ext: str):
    # 战法立绘按要求保存为 /resources/skin/skill/<cfg_id><ext>
    if category == 'skill':
        return f"/resources/skin/skill/{cfg_id}{ext}"
    # 其他分类沿用原结构 /resources/skin/<category>/<cfg_id>/default<ext>
    return f"/resources/skin/{category}/{cfg_id}/default{ext}"

def _target_paths(category: str, cfg_id: int, ext: str):
    base_dir = os.path.abspath(os.path.join(BASE_SKIN_DIR))
    if category == 'skill':
        # 战法立绘直接保存在 /resources/skin/skill 目录下，文件名为 <cfg_id><ext>
        target_dir = os.path.join(base_dir, 'skill')
        _ensure_dir(target_dir)
        target_file = os.path.join(target_dir, f"{cfg_id}{ext}")
        return target_dir, target_file
    # 其他分类沿用原结构
    target_dir = os.path.join(base_dir, category, str(cfg_id))
    _ensure_dir(target_dir)
    target_file = os.path.join(target_dir, f"default{ext}")
    return target_dir, target_file

def save_portrait(category: str, cfg_id: int, file_storage):
    """
    Save portrait image under resources/skin/<category>/<cfg_id>/default.<ext>
    Returns public URL string on success, or (None, error) on failure.
    """
    if not file_storage:
        return None, 'No file provided'

    ext = _ext_from_filename(file_storage.filename)
    if ext is None:
        return None, 'Unsupported file type; only png/jpg/jpeg are allowed'

    _, target_file = _target_paths(category, cfg_id, ext)
    try:
        file_storage.save(target_file)
    except Exception as e:
        return None, f'Failed to save file: {e}'

    public_url = _build_public_url(category, cfg_id, ext)
    return public_url, None