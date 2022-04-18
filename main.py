from scripts.count_playlist_time import count_playlist_time
from scripts.stalk_channel import stalkChannel
from scripts.vars import vars
import os

#inicia software, main thread
if __name__ == "__main__":
    os.system("cls")
    try:
        stalkChannel.get_all_comments_from_target("https://www.youtube.com/user/PewDiePie", 0)
    except:
        print("ALGUM ERRO OCORREU DURANTE A EXECUÇÃO DA FUNÇÃO!")
        print("AGUARDE!")
    vars.webdriver.quit()
    print("WEBDRIVER FECHADO!")