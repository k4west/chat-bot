import discord
from discord.ext import commands


class LevelButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=10)
        self.level = ""

    @discord.ui.button(label="직접입력", style=discord.ButtonStyle.secondary, row=0)
    async def direct(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "직접입력을 누르셨습니다", delete_after=5
        )
        self.level = ""

    @discord.ui.button(label="Bronze", style=discord.ButtonStyle.danger, row=1)
    async def Bronze(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Bronze을 누르셨습니다", delete_after=5)
        # # interaction.extras['Bronze'] = '1~5'
        self.level = "1~5"

    @discord.ui.button(label="Silver", style=discord.ButtonStyle.secondary, row=1)
    async def Silver(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Silver을 누르셨습니다", delete_after=5)
        self.level = "6~10"

    @discord.ui.button(label="Gold", style=discord.ButtonStyle.primary, row=2)
    async def Gold(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Gold을 누르셨습니다", delete_after=5)
        self.level = "11~15"

    @discord.ui.button(label="Platinum", style=discord.ButtonStyle.green, row=2)
    async def Platinum(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Platinum을 누르셨습니다", delete_after=5
        )
        self.level = "16~20"

    @discord.ui.button(label="Diamond", style=discord.ButtonStyle.secondary, row=3)
    async def Diamond(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Diamond을 누르셨습니다", delete_after=5
        )
        self.level = "21~25"

    @discord.ui.button(label="Ruby", style=discord.ButtonStyle.danger, row=3)
    async def Ruby(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Ruby 누르셨습니다", delete_after=5)
        self.level = "26~30"


# import discord
# from discord.ext import commands


# class LevelButton(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=10)
#         self.add_item(a := discord.ui.Button(label="직접 입력"))
#         self.add_item(
#             b := discord.ui.Button(
#                 label="Bronze", style=discord.ButtonStyle.danger, row=1
#             )
#         )
#         self.add_item(
#             c := discord.ui.Button(
#                 label="Silver", style=discord.ButtonStyle.secondary, row=1
#             )
#         )
#         self.add_item(
#             d := discord.ui.Button(
#                 label="Gold", style=discord.ButtonStyle.primary, row=2
#             )
#         )
#         self.add_item(
#             e := discord.ui.Button(
#                 label="Platinum", style=discord.ButtonStyle.green, row=2
#             )
#         )
#         self.add_item(
#             f := discord.ui.Button(
#                 label="Diamond", style=discord.ButtonStyle.primary, row=3
#             )
#         )
#         self.add_item(
#             g := discord.ui.Button(
#                 label="Ruby", style=discord.ButtonStyle.danger, row=3
#             )
#         )

#         self.levels = (i for i in (a, b, c, d, e, f, g))
