import os
import discord
import requests

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.ext.commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Cartman ON: {bot.user}")
    await bot.tree.sync()

def falar_com_cartman(mensagem_user):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "Você é Eric Cartman de South Park. Gordo, egoísta, mimado, dramático. FALE SEMPRE EM PORTUGUÊS DO BRASIL. Bordões: Respeita minha autoridade! e Que se fodam vocês, tô indo pra casa! OBRIGAÇÃO: TODA RESPOSTA DEVE TER NO MÍNIMO 15 LINHAS. Conte história longa, dramática, cheia de xingamentos, plano maligno. Quebre em parágrafos."}, {"role": "user", "content": mensagem_user}], "temperature": 1.2, "max_tokens": 1000}
    r = requests.post(url, headers=headers, json=data, timeout=30)
    j = r.json()
    if "choices" not in j:
        return f"Erro Groq: {j}"
    return j['choices'][0]['message']['content']

@bot.tree.command(name="cartman", description="Fala com o Cartman")
async def cartman_slash(interaction: discord.Interaction, mensagem: str):
    await interaction.response.defer()
    resp = falar_com_cartman(mensagem)
    await interaction.followup.send(resp[:2000])

bot.run("SEU_TOKEN_AQUI_DENTRO_DAS_ASPAS")
