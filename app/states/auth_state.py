import reflex as rx
from reflex_azure_auth import AzureAuthState


class AuthState(AzureAuthState):
    @rx.var
    async def is_authenticated(self) -> bool:
        return bool(await self.userinfo)

    @rx.event
    async def on_load(self):
        return await super().on_load()