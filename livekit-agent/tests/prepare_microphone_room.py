#!/usr/bin/env python3
"""Prepare a temporary LiveKit room and short-lived browser microphone token.

Run from the Mac mini with the mission venv. API credentials are read from the
private project .env and are never printed. Press Ctrl+C to delete the room.
"""
import argparse
import asyncio
import json
import uuid
from pathlib import Path


def read_env(path: Path) -> dict[str, str]:
    values = {}
    for line in path.read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("\"'")
    return values


async def prepare(project: Path) -> None:
    from livekit import api

    env = read_env(project / ".env")
    ws_url = env["LIVEKIT_URL"]
    api_url = ws_url.replace("wss://", "https://").replace("ws://", "http://")
    client = api.LiveKitAPI(
        url=api_url,
        api_key=env["LIVEKIT_API_KEY"],
        api_secret=env["LIVEKIT_API_SECRET"],
    )
    room_name = "physical23-" + uuid.uuid4().hex[:10]
    token = (
        api.AccessToken(env["LIVEKIT_API_KEY"], env["LIVEKIT_API_SECRET"])
        .with_identity("physical-microphone")
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
            )
        )
        .to_jwt()
    )
    try:
        await client.room.create_room(api.CreateRoomRequest(name=room_name))
        await client.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(agent_name="jarvis-agent", room=room_name)
        )
        print(
            json.dumps(
                {"url": ws_url, "room": room_name, "identity": "physical-microphone", "token": token},
                ensure_ascii=False,
            ),
            flush=True,
        )
        print("Collez url et token dans le client navigateur; Ctrl+C supprime la salle.", flush=True)
        await asyncio.Event().wait()
    finally:
        try:
            await client.room.delete_room(api.DeleteRoomRequest(room=room_name))
        finally:
            await client.aclose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project",
        type=Path,
        default=Path("/var/lib/jarvis/projects/mission23/livekit-agent"),
    )
    asyncio.run(prepare(parser.parse_args().project))
