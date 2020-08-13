from vkbottle.bot import Blueprint
from vkbottle.types import GroupJoin
bp = Blueprint(name="Event запросы")


@bp.on.event.group_join()
async def group_join(event: GroupJoin):
    await bp.api.messages.send(
        peer_id=event.user_id,
        message="Добро пожаловать к нам в сообщество!",
        random_id=bp.extension.random_id()
    )