from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


class QwenToolkit:
    """Reusable Qwen inference helpers for scripts and CLI usage."""

    IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
    VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

    @staticmethod
    def collect_inputs(
        input_path: str | Path,
        input_type: str = "auto",
        allowed_exts: set[str] | None = None,
    ) -> list[Path]:
        path = Path(input_path)

        if input_type == "auto":
            if path.is_dir():
                input_type = "dir"
            elif path.suffix.lower() == ".txt":
                input_type = "txt"
            else:
                input_type = "file"

        if input_type == "dir":
            if not path.exists():
                raise FileNotFoundError(f"Input directory not found: {path}")
            files = sorted([p for p in path.iterdir() if p.is_file()])
        elif input_type == "txt":
            if not path.exists():
                raise FileNotFoundError(f"Input txt not found: {path}")
            files = []
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    raw = line.strip()
                    if not raw:
                        continue
                    files.append(Path(raw))
        elif input_type == "file":
            files = [path]
        else:
            raise ValueError(f"Unsupported input_type: {input_type}")

        if allowed_exts:
            files = [p for p in files if p.suffix.lower() in allowed_exts]
        return files

    @staticmethod
    def _append_line(output_txt: str | Path, line: str) -> Path:
        out = Path(output_txt)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("a", encoding="utf-8") as f:
            f.write(line)
        return out

    @staticmethod
    def qwen2vl_infer_images(
        model_path: str,
        images: Iterable[str | Path],
        prompt: str,
        output_txt: str | Path,
        max_new_tokens: int = 128,
    ) -> Path:
        try:
            import torch
            from transformers import AutoProcessor, Qwen2VLForConditionalGeneration
            from qwen_vl_utils import process_vision_info
        except Exception as e:
            raise ImportError("Qwen2-VL inference requires torch, transformers, and qwen-vl-utils.") from e

        model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_path,
            torch_dtype="auto",
            device_map="auto",
        )
        processor = AutoProcessor.from_pretrained(model_path)
        device = "cuda" if torch.cuda.is_available() else "cpu"

        out_path = Path(output_txt)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("", encoding="utf-8")

        for image_path in images:
            image_path = str(image_path)
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image_path},
                        {"type": "text", "text": prompt},
                    ],
                }
            ]

            text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            image_inputs, _ = process_vision_info(messages)
            inputs = processor(
                text=[text],
                images=image_inputs,
                padding=True,
                return_tensors="pt",
            )
            inputs = inputs.to(device)

            generated_ids = model.generate(**inputs, max_new_tokens=max_new_tokens)
            trimmed = [out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
            output_text = processor.batch_decode(
                trimmed,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0].replace("\n", "")

            QwenToolkit._append_line(out_path, f"{image_path}#####{output_text}\n")

        return out_path

    @staticmethod
    def qwen3vl_infer_videos(
        model_path: str,
        videos: Iterable[str | Path],
        prompt: str,
        output_txt: str | Path,
        max_new_tokens: int = 128,
    ) -> Path:
        try:
            import torch
            from transformers import AutoModelForImageTextToText, AutoProcessor
        except Exception as e:
            raise ImportError("Qwen3-VL inference requires torch and transformers.") from e

        model = AutoModelForImageTextToText.from_pretrained(
            model_path,
            dtype=torch.bfloat16,
            device_map="auto",
        )
        model.eval()
        processor = AutoProcessor.from_pretrained(model_path)

        out_path = Path(output_txt)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("", encoding="utf-8")

        for video_path in videos:
            video_path = str(video_path)
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "video", "video": video_path},
                        {"type": "text", "text": prompt},
                    ],
                }
            ]

            inputs = processor.apply_chat_template(
                messages,
                tokenize=True,
                add_generation_prompt=True,
                return_dict=True,
                return_tensors="pt",
            )
            inputs = inputs.to(model.device)

            with torch.inference_mode():
                generated_ids = model.generate(**inputs, max_new_tokens=max_new_tokens)
                trimmed = [out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
                output_text = processor.batch_decode(
                    trimmed,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=False,
                )[0].replace("\n", "")

            QwenToolkit._append_line(out_path, f"{video_path}#####{output_text}\n")

        return out_path

    @staticmethod
    def qwen3_text_refine_from_csv(
        model_path: str,
        input_csv: str | Path,
        output_txt: str | Path,
        image_desc_field: str,
        camera_desc_field: str,
        question: str,
        id_field: str = "video_pth",
        max_new_tokens: int = 2048,
        strip_before_token_id: int | None = None,
    ) -> Path:
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except Exception as e:
            raise ImportError("Qwen3 text inference requires torch and transformers.") from e

        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype="auto",
            device_map="auto",
        )

        rows: list[dict[str, str]] = []
        with Path(input_csv).open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)

        out = Path(output_txt)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("", encoding="utf-8")

        for idx, row in enumerate(rows):
            image_description = row.get(image_desc_field, "")
            camera_description = row.get(camera_desc_field, "")
            data_id = row.get(id_field, str(idx))

            prompt_template = (
                f"Image description: {image_description} "
                f"Camera description: {camera_description} {question}"
            )
            messages = [{"role": "user", "content": prompt_template}]
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

            generated_ids = model.generate(**model_inputs, max_new_tokens=max_new_tokens)
            output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()

            if strip_before_token_id is not None and strip_before_token_id in output_ids:
                last_idx = len(output_ids) - output_ids[::-1].index(strip_before_token_id)
                output_ids = output_ids[last_idx:]

            content = tokenizer.decode(output_ids, skip_special_tokens=True).replace("\n", "")
            line = f"{data_id}#####{image_description}#####{camera_description}#####{content}\n"
            QwenToolkit._append_line(out, line)

        return out

    @staticmethod
    def build_metadata_csv_from_pair_texts(
        image_caption_txt: str | Path,
        camera_caption_txt: str | Path,
        output_csv: str | Path,
        image_index_filter: int = 0,
    ) -> Path:
        camera_map: dict[str, dict[str, str]] = {}
        with Path(camera_caption_txt).open("r", encoding="utf-8") as f:
            for line in f:
                raw = line.strip()
                if not raw or "#####" not in raw:
                    continue
                video_pth, camera_caption = raw.split("#####", 1)
                video_name = Path(video_pth).stem
                camera_map[video_name] = {
                    "video_pth": video_pth,
                    "camera_description": camera_caption,
                }

        records: list[dict[str, str]] = []
        with Path(image_caption_txt).open("r", encoding="utf-8") as f:
            for line in f:
                raw = line.strip()
                if not raw or "#####" not in raw:
                    continue
                image_pth, image_caption = raw.split("#####", 1)
                image_path = Path(image_pth)
                try:
                    image_index = int(image_path.stem)
                except ValueError:
                    continue

                if image_index != image_index_filter:
                    continue

                data_name = image_path.parent.name
                camera_data = camera_map.get(data_name)
                if not camera_data:
                    continue

                if not Path(image_pth).exists() or not Path(camera_data["video_pth"]).exists():
                    continue

                records.append(
                    {
                        "data_name": data_name,
                        "video_pth": camera_data["video_pth"],
                        "first_frame_pth": image_pth,
                        "image_description": image_caption,
                        "camera_description": camera_data["camera_description"],
                    }
                )

        out = Path(output_csv)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "data_name",
                "video_pth",
                "first_frame_pth",
                "image_description",
                "camera_description",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in records:
                writer.writerow(item)

        return out
