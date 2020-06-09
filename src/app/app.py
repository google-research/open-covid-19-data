#!/usr/bin/python
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import asyncio
import json
import os
import time
from datetime import datetime

import pandas as pd
from tornado import web
from tornado.options import define, options

import aiohttp

CURRENT_DIR = os.path.dirname(__file__)
URL_PREFIX = "https://docs.google.com/spreadsheets/d"
SHEET_ID = "1ilFQ3RayHutnhM5dMUuyxjY-e5YZWe-28tuVECBzyGU"
SHEET_GID = "1397523392"

define("port", default=8888, help="port to listen on")
define("root", default=CURRENT_DIR, help="root dir for templates")
define("cache_interval", default=20, help="cache interval in seconds")


# Global cached data.
CACHED_DATA = []
# Global last update timestamp
LAST_UPDATED = None


def formatData(data):
    df = pd.read_csv(io.StringIO(data))
    codes = pd.read_csv(os.path.join(CURRENT_DIR, "country-codes.csv"))
    codes = (
        codes[["ISO3166-1-Alpha-3", "ISO3166-1-numeric"]]
        .dropna()
        .rename(
            {"ISO3166-1-Alpha-3": "region_code", "ISO3166-1-numeric": "numeric_code"},
            axis=1,
        )
        .astype({"numeric_code": "int"})
    )
    merged = df.merge(codes, on="region_code")
    global CACHED_DATA
    CACHED_DATA = merged.to_json(orient="records")
    global LAST_UPDATED
    LAST_UPDATED = int(time.time())


async def fetchRemoteData():
    url = f"{URL_PREFIX}/{SHEET_ID}/export?format=csv&id={SHEET_ID}&gid={SHEET_GID}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.text()
            formatData(data)


async def fetchData():
    now = int(time.time())
    if not LAST_UPDATED or (LAST_UPDATED + options.cache_interval) < now:
        await fetchRemoteData()
    return json.loads(CACHED_DATA)


class DataHandler(web.RequestHandler):
    """Serves requests for data."""

    async def get(self):
        self.set_header("Content-Type", "application/json")
        self.write(
            {
                "data": await fetchData(),
                "last_updated": datetime.fromtimestamp(LAST_UPDATED).strftime(
                    "%d %b %Y %H:%M:%S"
                ),
            }
        )
        self.finish()


async def map():
    app = web.Application(
        [
            ("/data.json", DataHandler),
            (
                r"/(.*)",
                web.StaticFileHandler,
                {"path": options.root, "default_filename": "index.html"},
            ),
        ]
    )
    app.listen(options.port)
    print(f"Listening on http://localhost:{options.port}")


async def steamlit():
    cmd = ["streamlit", "run", "./src/views/main.py", "--server.headless", "true"]
    process = await asyncio.create_subprocess_exec(
        cmd[0], *cmd[1:], stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    print(f"started streamlit process: {process.pid}")
    return await process.wait()


async def main():
    await (asyncio.gather(fetchRemoteData(), steamlit(), map()))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
