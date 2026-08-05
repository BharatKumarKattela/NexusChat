

class OnlineCommand:
    def __init__(self, manager):
        self.manager = manager

    async def execute(self, session):
        users = self.manager.get_online_users()

        response = (
            f"Online Users ({len(users)})\n"
            + "\n".join(f"• {user}" for user in users)
        )
        await self.manager.send_to(session, response)