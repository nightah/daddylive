import json
import base64

name = "daddylive-channels"

def json_to_m3u8(json_path, output_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f'#EXTM3U url-tvg="https://raw.githubusercontent.com/nightah/daddylive/refs/heads/main/epgs/{name}-epg.xml"\n\n')

        for channel_name, info in data.items():
            group = info.get("group_title", "")
            tvg_id = info.get("tvg_id", "")
            tvg_logo = info.get("tvg_logo", "")
            stream_url = info.get("stream_url", "")
            options = info.get("options", [])

            extinf = f'#EXTINF:-1 group-title="{group}" tvg-id="{tvg_id}" tvg-logo="{tvg_logo}",{channel_name}'
            f.write(f"{extinf}\n")

            for opt in options:
                f.write(f"{opt}\n")

            encoded_url = base64.urlsafe_b64encode(stream_url.encode()).decode().rstrip('=')
            f.write(f"https://example.com/watch/{encoded_url}.m3u8\n\n")

if __name__ == "__main__":
    json_to_m3u8(f"../{name}-data.json", f"../{name}.m3u8")
