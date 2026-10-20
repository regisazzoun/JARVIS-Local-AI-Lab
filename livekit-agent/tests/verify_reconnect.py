#!/usr/bin/env python3
"""Integration check that an independent WebRTC client can reconnect and redispatch JARVIS."""
import argparse
import asyncio
import json
import time
import uuid
from pathlib import Path


def read_env(path):
    values = {}
    for line in path.read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("\"'")
    return values


async def main(args):
    from livekit import api, rtc

    env = read_env(args.project / ".env")
    ws_url = args.url or env["LIVEKIT_URL"]
    api_url = ws_url.replace("wss://", "https://").replace("ws://", "http://")
    lkapi = api.LiveKitAPI(
        url=api_url,
        api_key=env["LIVEKIT_API_KEY"],
        api_secret=env["LIVEKIT_API_SECRET"],
    )
    room_name = "reconnect23-" + uuid.uuid4().hex[:10]
    rooms = []
    started = time.monotonic()

    async def connect_client(identity):
        token = (
            api.AccessToken(env["LIVEKIT_API_KEY"], env["LIVEKIT_API_SECRET"])
            .with_identity(identity)
            .with_grants(api.VideoGrants(room_join=True, room=room_name))
            .to_jwt()
        )
        room = rtc.Room()
        await asyncio.wait_for(room.connect(ws_url, token), timeout=30)
        rooms.append(room)
        return room

    async def wait_agent_api(present, timeout=60):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            response = await lkapi.room.list_participants(api.ListParticipantsRequest(room=room_name))
            identities = [participant.identity for participant in response.participants]
            found = any(identity.startswith("agent-") for identity in identities)
            if found == present:
                return identities
            await asyncio.sleep(0.25)
        return None


    try:
        await lkapi.room.create_room(api.CreateRoomRequest(name=room_name))
        await lkapi.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(agent_name="jarvis-agent", room=room_name)
        )
        first = await connect_client("reconnect-verifier-1")
        assert await wait_agent_api(True), "agent did not join first connection"
        first_joined = time.monotonic() - started
        await first.disconnect()
        assert await wait_agent_api(False, timeout=25) is not None, "agent did not leave after client disconnect"
        disconnected = time.monotonic() - started
        second = await connect_client("reconnect-verifier-2")
        await lkapi.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(agent_name="jarvis-agent", room=room_name)
        )
        participants = await wait_agent_api(True)
        assert participants is not None, "agent did not rejoin after client reconnect"
        rejoined = time.monotonic() - started
        result = {
            "check": "livekit_client_disconnect_reconnect_agent_redispatch",
            "verified": True,
            "physical_microphone": False,
            "room": room_name,
            "first_agent_join_s": first_joined,
            "agent_left_s": disconnected,
            "agent_rejoined_s": rejoined,
            "participant_after_reconnect": participants,
        }
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(result, ensure_ascii=False))
    finally:
        for room in rooms:
            try:
                await room.disconnect()
            except Exception:
                pass
        try:
            await lkapi.room.delete_room(api.DeleteRoomRequest(room=room_name))
        finally:
            await lkapi.aclose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=Path("/var/lib/jarvis/projects/mission23/livekit-agent"))
    parser.add_argument("--url")
    parser.add_argument("--output", type=Path, required=True)
    asyncio.run(main(parser.parse_args()))
