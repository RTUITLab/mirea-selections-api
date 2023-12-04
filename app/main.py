import qrcode
import asyncio
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import VerticalGradiantColorMask

import asyncio
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware

from app.settings import settings
from app.routers.auth_router import auth_router
from app.routers.votings_router import votings_router


app = FastAPI(openapi_url=settings.api_prefix,
              docs_url=f'{settings.api_prefix}/docs')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(votings_router, prefix=settings.api_prefix)


@app.get(f'{settings.api_prefix}/__health')
async def healthcheck():
    def gen_picture():
        qr = qrcode.QRCode(
            error_correction=qrcode.ERROR_CORRECT_M, box_size=20, border=1)
        qr.add_data('data')
        qr.make(fit=True)
        img = qr.make_image(
            fill_color="White",
            back_color="Transparent",
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            eye_drawer=RoundedModuleDrawer(),
            embeded_image_path='logo.png',
            color_mask=VerticalGradiantColorMask(
                top_color=((120, 0, 0)), bottom_color=((79, 1, 10)))
        )
        print(img.get_image().save('aa.png'))

    await asyncio.to_thread(gen_picture)
    return {}


@app.get(f'{settings.api_prefix}/')
async def test_sse(req: Request) -> EventSourceResponse:
    async def event_generator():
        count = 0
        while True:
            if await req.is_disconnected():
                print('Client disconnected')
                break

            print(count)
            yield {'data': count, 'retry': 1}
            count += 1

            await asyncio.sleep(1)

    return EventSourceResponse(event_generator())
