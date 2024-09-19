import asyncio

from app.tokens import AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, REDIRECT_URI, AZURE_REFRESH_TOKEN
from aiohttp import ClientSession
from spnkr import HaloInfiniteClient, AzureApp, refresh_player_tokens, authenticate_player
from spnkr.film import read_highlight_events


app = AzureApp(AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, REDIRECT_URI)


async def get_xbl_client(app):
    async with ClientSession() as session:
        player = await refresh_player_tokens(session, app, AZURE_REFRESH_TOKEN)
        print(f"Refresing player tokens. Player is valid: {player.is_valid}")
        return player


player = asyncio.run(get_xbl_client(app))


async def main():

    async with ClientSession() as session:
        # refresh_token = await authenticate_player(session, app)
        # print(refresh_token)
        if not player.is_valid:
            await get_xbl_client(app)

        client = HaloInfiniteClient(
            session=session,
            spartan_token=f"{player.spartan_token.token}",
            clearance_token=f"{player.clearance_token.token}",
            # Optional, default rate is 5.
            requests_per_second=5,
        )

        yield client


def get_client():
    awaitable = anext(main())
    return awaitable


async def get_match(match_id):
    awaitable = get_client()
    client = await awaitable
    resp = await client.stats.get_match_stats(match_id)
    match_stats = await resp.parse()
    return match_stats


async def get_match_history(gamer_tag, count=25, start=0, match_type="all"):
    awaitable = get_client()
    client = await awaitable
    resp = await client.stats.get_match_history(gamer_tag, start=start, count=count, match_type=match_type)
    match_history = await resp.parse()
    return match_history.results


async def get_user(gamer_tag):
    awaitable = get_client()
    client = await awaitable
    resp = await client.profile.get_user_by_gamertag(gamer_tag)
    user = await resp.parse()
    return user


async def get_users_for_xuids(xuids):
    awaitable = get_client()
    client = await awaitable
    resp = await client.profile.get_users_by_id(xuids)
    users = await resp.parse()
    return users


async def get_gamemode(asset_id, version_id):
    awaitable = get_client()
    client = await awaitable
    resp = await client.discovery_ugc.get_ugc_game_variant(asset_id, version_id)
    gamemode = await resp.parse()
    return gamemode


async def get_map(asset_id, version_id):
    awaitable = get_client()
    client = await awaitable
    resp = await client.discovery_ugc.get_map(asset_id, version_id)
    map_data = await resp.parse()
    return map_data


async def get_film(match_id):
    awaitable = get_client()
    client = await awaitable
    events = await read_highlight_events(client, match_id)
    return events
