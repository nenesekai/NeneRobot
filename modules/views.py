from discord import ui, Interaction


class ForceRebindView(ui.View):
    def __init__(self):
        super().__init__()
        self.value = False

    @ui.button(label='替换并绑定')
    async def confirm(self, interaction:Interaction, button:ui.Button):
        self.value = True
        self.stop()
        await interaction.response.defer()
