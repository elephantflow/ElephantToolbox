from __future__ import annotations

import argparse
import os

from boxsdk import Client, JWTAuth


"""Upload local file to Box cloud with JWT auth.

Note: Requires valid Box app credentials and jwt config.
"""


def upload_file(client_id: str, client_secret: str, local_file_path: str, folder_id: str = "0") -> str:
    jwt_auth = JWTAuth(client_id, client_secret)
    auth_token = jwt_auth.authenticate()
    client = Client(auth_token)

    if not os.path.isfile(local_file_path):
        raise FileNotFoundError(f"Local file not found: {local_file_path}")

    box_file_name = os.path.basename(local_file_path)
    with open(local_file_path, 'rb') as file:
        uploaded_file = client.folder(folder_id=folder_id).upload(box_file_name, file)
    return uploaded_file.object_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload file to Box cloud.")
    parser.add_argument("--client_id", required=True)
    parser.add_argument("--client_secret", required=True)
    parser.add_argument("--local_file", required=True)
    parser.add_argument("--folder_id", default="0")
    args = parser.parse_args()

    file_id = upload_file(args.client_id, args.client_secret, args.local_file, args.folder_id)
    print(f"File uploaded to Box with ID: {file_id}")


if __name__ == "__main__":
    main()
