from __future__ import annotations

import csv
import random
from pathlib import Path


class DatasetMetadataToolkit:
    """Reusable dataset metadata builders for video/noise/prompt datasets."""

    VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"}

    @staticmethod
    def parse_delimited_pairs(txt_path: str | Path, separator: str = "#####") -> list[tuple[str, str]]:
        txt_path = Path(txt_path)
        if not txt_path.exists():
            raise FileNotFoundError(f"txt file not found: {txt_path}")

        pairs: list[tuple[str, str]] = []
        with txt_path.open("r", encoding="utf-8") as f:
            for line in f:
                raw = line.strip()
                if not raw or separator not in raw:
                    continue
                left, right = raw.split(separator, 1)
                pairs.append((left.strip(), right.strip()))
        return pairs

    @staticmethod
    def write_csv_rows(output_csv: str | Path, fieldnames: list[str], rows: list[dict[str, str]]) -> tuple[Path, int]:
        output_csv = Path(output_csv)
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        with output_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return output_csv, len(rows)

    @classmethod
    def load_prompt_map_from_txt(
        cls,
        txt_path: str | Path,
        separator: str = "#####",
        key_mode: str = "stem",
        path_part_index: int | None = None,
    ) -> dict[str, str]:
        pairs = cls.parse_delimited_pairs(txt_path, separator=separator)
        prompt_map: dict[str, str] = {}
        for left, right in pairs:
            p = Path(left)
            if key_mode == "stem":
                key = p.stem
            elif key_mode == "parent":
                key = p.parent.name
            elif key_mode == "path_part":
                parts = [x for x in left.replace("\\", "/").split("/") if x]
                if path_part_index is None:
                    raise ValueError("path_part_index is required when key_mode='path_part'.")
                if path_part_index < -len(parts) or path_part_index >= len(parts):
                    continue
                key = parts[path_part_index]
                key = key.split(".")[0]
            else:
                raise ValueError("key_mode must be one of: stem, parent, path_part")
            prompt_map[key] = right
        return prompt_map

    @classmethod
    def scan_videos(cls, video_root: str | Path, recursive: bool = False) -> list[Path]:
        video_root = Path(video_root)
        if not video_root.exists():
            raise FileNotFoundError(f"video_root not found: {video_root}")

        pattern = "**/*" if recursive else "*"
        files = [p for p in video_root.glob(pattern) if p.is_file() and p.suffix.lower() in cls.VIDEO_EXTS]
        return sorted(files)

    @classmethod
    def build_video_prompt_noise_csv_from_prompt_map(
        cls,
        video_root: str | Path,
        prompt_map: dict[str, str],
        output_csv: str | Path,
        recursive: bool = True,
        video_path_mode: str = "absolute",
        video_path_prefix: str = "videos",
        noise_from_video_replace_from: str = "videos",
        noise_from_video_replace_to: str = "noises",
        noise_suffix_from: str = ".mp4",
        noise_suffix_to: str = "_noises.npy",
    ) -> tuple[Path, int]:
        videos = cls.scan_videos(video_root, recursive=recursive)
        rows: list[dict[str, str]] = []
        root = Path(video_root)

        for video in videos:
            key = video.stem
            prompt = prompt_map.get(key)
            if prompt is None:
                continue

            rel = video.relative_to(root).as_posix()
            if video_path_mode == "relative":
                video_value = f"{video_path_prefix}/{rel}"
            else:
                video_value = str(video)

            noise_value = video_value.replace(noise_from_video_replace_from, noise_from_video_replace_to)
            if noise_suffix_from:
                noise_value = noise_value.replace(noise_suffix_from, noise_suffix_to)

            rows.append(
                {
                    "video": video_value,
                    "camera_noise": noise_value,
                    "prompt": prompt,
                }
            )

        return cls.write_csv_rows(output_csv, ["video", "camera_noise", "prompt"], rows)

    @staticmethod
    def build_camera_noise_training_csv(
        video_root: str | Path,
        noise_root: str | Path,
        caption_metadata_txt: str | Path,
        output_csv: str | Path,
        separator: str = "#####",
        caption_key_mode: str = "stem",
        recursive: bool = False,
    ) -> tuple[Path, int]:
        video_root = Path(video_root)
        noise_root = Path(noise_root)
        if not noise_root.exists():
            raise FileNotFoundError(f"noise_root not found: {noise_root}")
        caption_map = DatasetMetadataToolkit.load_prompt_map_from_txt(
            caption_metadata_txt,
            separator=separator,
            key_mode=caption_key_mode,
        )

        rows: list[dict[str, str]] = []
        for video_file in DatasetMetadataToolkit.scan_videos(video_root, recursive=recursive):
            video_name = video_file.stem
            if video_name not in caption_map:
                continue

            noise_file = noise_root / f"{video_name}_noises.npy"
            if not noise_file.exists():
                continue

            rows.append(
                {
                    "video": str(video_file),
                    "camera_noise": str(noise_file),
                    "prompt": caption_map[video_name],
                }
            )
        return DatasetMetadataToolkit.write_csv_rows(output_csv, ["video", "camera_noise", "prompt"], rows)

    @staticmethod
    def build_multicam_training_csv_from_description_txt(
        description_txt: str | Path,
        multicam_train_root: str | Path,
        noise_root: str | Path,
        output_csv: str | Path,
        separator: str = "#####",
        skip_noise_names: set[str] | None = None,
        check_exists: bool = False,
    ) -> tuple[Path, int]:
        pairs = DatasetMetadataToolkit.parse_delimited_pairs(description_txt, separator=separator)
        multicam_train_root = Path(multicam_train_root)
        noise_root = Path(noise_root)
        skip_noise_names = skip_noise_names or set()

        rows: list[dict[str, str]] = []
        for video_ref, prompt in pairs:
            parts = [x for x in video_ref.replace("\\", "/").split("/") if x]
            if len(parts) < 4:
                continue
            fake_npy_name = f"{parts[-4]}_{parts[-3]}_{parts[-2]}_noises.npy"
            if fake_npy_name in skip_noise_names:
                continue

            video_pth = multicam_train_root / parts[-4] / parts[-3] / "videos" / f"{parts[-2]}.mp4"
            noise_pth = noise_root / fake_npy_name
            if check_exists and (not video_pth.exists() or not noise_pth.exists()):
                continue

            rows.append({"video": str(video_pth), "camera_noise": str(noise_pth), "prompt": prompt})

        return DatasetMetadataToolkit.write_csv_rows(output_csv, ["video", "camera_noise", "prompt"], rows)

    @staticmethod
    def build_multicam_with_reference_csv_from_ann_txt(
        ann_txt: str | Path,
        video_root: str | Path,
        noise_root: str | Path,
        output_csv: str | Path,
        separator: str = "#####",
        camera_count: int = 10,
        random_seed: int = 42,
        max_rows: int | None = None,
    ) -> tuple[Path, int]:
        pairs = DatasetMetadataToolkit.parse_delimited_pairs(ann_txt, separator=separator)
        video_root = Path(video_root)
        noise_root = Path(noise_root)
        rng = random.Random(random_seed)

        rows: list[dict[str, str]] = []
        for video_pth_raw, prompt in pairs:
            parts = [x for x in video_pth_raw.replace("\\", "/").split("/") if x]
            if len(parts) < 4:
                continue

            video_name = Path(parts[-1]).stem
            if not video_name.startswith("cam"):
                continue
            try:
                video_index = int(video_name.replace("cam", ""))
            except ValueError:
                continue

            noise_name = f"{parts[-4]}_{parts[-3]}_{video_name}_noises.npy"
            noise_pth = noise_root / noise_name

            candidate_indices = [i for i in range(1, camera_count + 1) if i != video_index]
            if not candidate_indices:
                continue
            ref_index = rng.choice(candidate_indices)
            reference_video = video_root / parts[-4] / parts[-3] / "videos" / f"cam{str(ref_index).zfill(2)}.mp4"

            rows.append(
                {
                    "video": video_pth_raw,
                    "reference_video": str(reference_video),
                    "camera_noise": str(noise_pth),
                    "prompt": prompt,
                }
            )
            if max_rows is not None and len(rows) >= max_rows:
                break

        return DatasetMetadataToolkit.write_csv_rows(output_csv, ["video", "reference_video", "camera_noise", "prompt"], rows)

    @staticmethod
    def build_multicam_all_cams_csv_from_prompt_txt(
        prompt_txt: str | Path,
        video_root: str | Path,
        noise_root: str | Path,
        output_csv: str | Path,
        separator: str = "#####",
        camera_count: int = 10,
        check_exists: bool = True,
    ) -> tuple[Path, int]:
        pairs = DatasetMetadataToolkit.parse_delimited_pairs(prompt_txt, separator=separator)
        video_root = Path(video_root)
        noise_root = Path(noise_root)

        rows: list[dict[str, str]] = []
        for image_ref, prompt in pairs:
            image_stem = Path(image_ref).stem
            parts = image_stem.split("_")
            if len(parts) < 3:
                continue

            folder_a = f"{parts[0]}_{parts[1]}"
            folder_b = parts[2]
            video_dir = video_root / folder_a / folder_b / "videos"

            for i in range(1, camera_count + 1):
                cam = f"cam{str(i).zfill(2)}"
                video_pth = video_dir / f"{cam}.mp4"
                noise_pth = noise_root / f"{folder_a}_{folder_b}_{cam}_noises.npy"
                if check_exists and (not video_pth.exists() or not noise_pth.exists()):
                    continue
                rows.append(
                    {
                        "video": str(video_pth),
                        "camera_noise": str(noise_pth),
                        "prompt": prompt,
                    }
                )

        return DatasetMetadataToolkit.write_csv_rows(output_csv, ["video", "camera_noise", "prompt"], rows)

    @staticmethod
    def build_openvid_camera_noise_csv(
        source_csv: str | Path,
        video_root: str | Path,
        noise_root: str | Path,
        output_csv: str | Path,
        video_field: str = "video",
        caption_field: str = "caption",
        require_noise_exists: bool = True,
    ) -> tuple[Path, int]:
        source_csv = Path(source_csv)
        video_root = Path(video_root)
        noise_root = Path(noise_root)

        if not source_csv.exists():
            raise FileNotFoundError(f"source_csv not found: {source_csv}")

        rows: list[dict[str, str]] = []
        with source_csv.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for item in reader:
                video_name = item.get(video_field, "")
                caption = item.get(caption_field, "")
                if not video_name:
                    continue

                video_pth = video_root / video_name
                noise_pth = noise_root / video_name.replace(".mp4", "_noises.npy")

                if not video_pth.exists():
                    continue
                if require_noise_exists and not noise_pth.exists():
                    continue

                rows.append(
                    {
                        "video": str(video_pth),
                        "camera_noise": str(noise_pth),
                        "prompt": caption,
                    }
                )

        return DatasetMetadataToolkit.write_csv_rows(output_csv, ["video", "camera_noise", "prompt"], rows)
