import json, random, discord

startup_message_sent = False

with open("data/Year 9.json", "r", encoding="utf-8") as f:
    ALL_QUESTIONS = json.load(f)

class QuizView(discord.ui.View):

    def __init__(self, questions, user):
        super().__init__(timeout=3600)
        self.questions = questions
        self.user = user
        self.index = 0
        self.results = []

    def make_question_embed(self):
        question = self.questions[self.index]
        embed = discord.Embed(
            title=question["question"],
            color=0x0075FF,
        )
        for letter, text in question["choices"].items():
            embed.add_field(name=letter, value=text, inline=False)
        embed.set_footer(text=f"Question {self.index + 1}/{len(self.questions)}")
        return embed

    def make_results_embed(self):
        correct_count = sum(1 for r in self.results if r[3])
        total = len(self.results)

        if correct_count == total:
            percentage = 100
        elif correct_count == 0:
            percentage = 0
        else:
            percentage = correct_count * 10 + random.randint(0, 9)

        embed = discord.Embed(
            title="Quiz Complete!",
            description=f"You scored **{correct_count}/{total}** ({percentage}%)",
            color=0x00C853 if correct_count >= total / 2 else 0xE53935,
        )
        for i, (question_text, chosen_text, reason, is_correct) in enumerate(self.results, start=1):
            mark = "\u2705" if is_correct else "\u274c"
            value = f"Your answer: **{chosen_text}**"
            if not is_correct:
                value += f" | Incorrect, {reason}"
            embed.add_field(name=f"{mark} Q{i}: {question_text}", value=value, inline=False)

        embed.set_footer(text=f"{self.user} (+{percentage} xp)")
        return embed

    async def answer(self, interaction: discord.Interaction, letter: str):
        question = self.questions[self.index]
        correct_letter = question["answer"]
        is_correct = letter == correct_letter
        chosen_text = question["choices"][letter]
        reason = question.get("reason", "")
        self.results.append((question["question"], chosen_text, reason, is_correct))

        self.index += 1

        if self.index < len(self.questions):
            await interaction.response.edit_message(embed=self.make_question_embed(), view=self)
        else:
            await interaction.response.edit_message(embed=self.make_results_embed(), view=None)
            self.stop()

    @discord.ui.button(label="A", style=discord.ButtonStyle.secondary)
    async def option_a(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.answer(interaction, "A")

    @discord.ui.button(label="B", style=discord.ButtonStyle.secondary)
    async def option_b(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.answer(interaction, "B")

    @discord.ui.button(label="C", style=discord.ButtonStyle.secondary)
    async def option_c(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.answer(interaction, "C")

    @discord.ui.button(label="D", style=discord.ButtonStyle.secondary)
    async def option_d(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.answer(interaction, "D")

class StartView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Click me", style=discord.ButtonStyle.green)
    async def click_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        questions = random.sample(ALL_QUESTIONS, min(10, len(ALL_QUESTIONS)))
        quiz_view = QuizView(questions, interaction.user)
        await interaction.response.send_message(
            embed=quiz_view.make_question_embed(), view=quiz_view, ephemeral=True
        )

async def on_ready():
    global startup_message_sent

    if not startup_message_sent:
        channel = bot.get_channel(1539992507792760842) or await bot.fetch_channel(1539992507792760842)

        embed = discord.Embed(
            title="Year 9 - Maths Test",
            description="Click the button and answer 10 maths questions in 60 minutes!",
            color=0x0075FF,
        )

        await channel.send(embed=embed, view=StartView())
        startup_message_sent = True

async def setup(bot_instance):
    global bot
    bot = bot_instance
    bot.add_listener(on_ready)
