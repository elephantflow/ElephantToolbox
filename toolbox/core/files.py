from __future__ import annotations

import random
from pathlib import Path

import requests


class FileToolkit:
    @staticmethod
    def download_url(url: str, output_path: str | Path | None = None) -> Path:
        response = requests.get(url, timeout=60)
        if response.status_code != 200:
            raise RuntimeError(f"Download failed: {url}, status={response.status_code}")

        output = Path(output_path) if output_path else Path(url.split("/")[-1])
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(response.content)
        return output

    @staticmethod
    def download_hf_repo(repo_id: str, local_dir: str | Path, allows: list[str] | None = None, ignores: list[str] | None = None) -> Path:
        from huggingface_hub import snapshot_download

        output = Path(local_dir)
        output.mkdir(parents=True, exist_ok=True)
        cache_dir = output / "cache"

        kwargs = {
            "cache_dir": str(cache_dir),
            "repo_id": repo_id,
            "local_dir": str(output),
            "local_dir_use_symlinks": False,
        }
        if allows:
            kwargs["allow_patterns"] = allows
        elif ignores:
            kwargs["ignore_patterns"] = ignores

        snapshot_download(**kwargs)
        return output

    @staticmethod
    def rename_randomized_sequential(folder_path: str | Path, suffix: str = ".mp4") -> int:
        base = Path(folder_path)
        subfolders = sorted([p for p in base.iterdir() if p.is_dir()])
        index = 0

        for subfolder in subfolders:
            files = [p for p in subfolder.iterdir() if p.is_file() and not p.name.startswith(".")]
            random.shuffle(files)
            for path in files:
                new_path = subfolder / f"{index:06d}{suffix}"
                path.rename(new_path)
                index += 1

        return index

    @staticmethod
    def batch_download_urls_from_file(url_file: str | Path, save_dir: str | Path) -> list[Path]:
        save_root = Path(save_dir)
        save_root.mkdir(parents=True, exist_ok=True)

        with open(url_file, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]

        saved: list[Path] = []
        for url in urls:
            file_name = url.split("/")[-1]
            path = FileToolkit.download_url(url, save_root / file_name)
            saved.append(path)
        return saved
