from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from main import error_details
from googleapiclient.discovery import build
from scripts.vars import vars
from colorama import Style, Fore
import traceback
import pickle
import json
import time
import os
import sys
import requests

class stalkChannel():

    #atualiza o youtube_api para usar a API_KEY desejada
    def update_youtube_api(index):
        vars.API_KEY_IN_USE = vars.API_KEYS[index]
        vars.youtube_api = build('youtube', 'v3', developerKey = vars.API_KEY_IN_USE)




    #verifica se existem api's que ainda possuem cota/quote
    def next_youtube_api():
        atual_api_index = vars.API_KEYS.index(vars.API_KEY_IN_USE)
        if (len(vars.API_KEYS) - 1) == atual_api_index:
            print("QUOTA DE TODA(S) A(S) API(S) ESGOTADA(S), CONFIGURE UMA NOVA 'API_KEY' OU ESPERA ATÉ MEIA NOITE PARA SUA QUOTA SER RESTAURADA!")
            raise Exception("QUOTA_DEPLETION")
        else:
            print(f"{Fore.YELLOW}{Style.BRIGHT}QUOTA DA API ATUAL FOI ESGOTADA, TENTANDO API DE INDEX = '{atual_api_index + 1}'!{Fore.WHITE}{Style.NORMAL}")
            stalkChannel.update_youtube_api(atual_api_index + 1)




    #busca por todos os canais em que o alvo é inscrito
    def get_followed_channels_of_target(target):
        vars.webdriver.get(f"{target}/channels")
        time.sleep(1)
        target_channel_name = vars.webdriver.find_element(by = By.XPATH, value = f"/html/body/ytm-app/div[1]/ytm-browse/ytm-c4-tabbed-header-renderer/div/div/h1").text
        print(f"\nNOME DO CANAL ALVO É = '{target_channel_name}'")
        videos_area = vars.webdriver.find_element(by = By.XPATH, value = f"/html/body")
        while True:
            try:
                for i in range(20):
                    videos_area.send_keys(Keys.PAGE_DOWN)
                time.sleep(2)
                show_more = vars.webdriver.find_element(by = By.XPATH, value = f"/html/body/ytm-app/div[1]/ytm-browse/ytm-single-column-browse-results-renderer/div[2]/div[4]/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/div/c3-next-continuation/c3-material-button/button")
                show_more.click()
                time.sleep(1)
            except:
                break
        followed_channels = []
        for i in range(1000):
            try:
                followed_channels.append(vars.webdriver.find_element(by = By.XPATH, value = f"/html/body/ytm-app/div[1]/ytm-browse/ytm-single-column-browse-results-renderer/div[2]/div[4]/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-channel-renderer[{i + 1}]/div/div/a").get_attribute("href"))
            except:
                break
        return target_channel_name, followed_channels




    #busca por todos os videos de um canal
    def get_all_videos_from_channel(channel_link):
        vars.webdriver.get(f"{channel_link}/videos")
        time.sleep(1)
        try:
            channel_name = vars.webdriver.find_element(by = By.XPATH, value = f"/html/body/ytm-app/div[1]/ytm-browse/ytm-c4-tabbed-header-renderer/div[2]/div/h1").text
        except:
            try:
                channel_name = vars.webdriver.find_element(by = By.XPATH, value = f"/html/body/ytm-app/ytm-mobile-topbar-renderer/header/div/h1").text
            except:
                channel_name = "cant_get_link"
        videos_area = vars.webdriver.find_element(by = By.XPATH, value = f"/html/body")
        for i in range(100):
            scrollbar_pos = int(vars.webdriver.execute_script("return window.pageYOffset"))
            for w in range(20):
                videos_area.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            #print(f"    scroll '{i + 1}', inicio = '{scrollbar_initial_pos}', final = '{scrollbar_end_pos}'")
            if scrollbar_pos == int(vars.webdriver.execute_script("return window.pageYOffset")):
                break
        channel_videos = []
        for i in range(10000):
            try:
                new_video = {}
                new_video["link"] = vars.webdriver.find_element(by = By.XPATH, value = f"/html/body/ytm-app/div[1]/ytm-browse/ytm-single-column-browse-results-renderer/div[2]/div[2]/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-video-renderer[{i + 1}]/div/div/a").get_attribute("href")
                new_video["title"] = vars.webdriver.find_element(by = By.XPATH, value = f"/html/body/ytm-app/div[1]/ytm-browse/ytm-single-column-browse-results-renderer/div[2]/div[2]/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-video-renderer[{i + 1}]/div/div/a/h4").text
                new_video["age"] = vars.webdriver.find_element(by = By.XPATH, value = f"/html/body/ytm-app/div[1]/ytm-browse/ytm-single-column-browse-results-renderer/div[2]/div[2]/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-video-renderer[{i + 1}]/div/div/a/div/div[2]").text
                channel_videos.append(new_video)
                print(f"novo video = '{new_video}'")
            except Exception as e:
                #error_details(str(traceback.format_exc()), str(e))
                break
        vars.webdriver.get("https://m.youtube.com/")
        return channel_name, channel_videos




    #busca pelos comentários de um vídeo
    def get_all_comments_from_video(video_link, open_reels = False, max_comments = 1000, exact_value = False):
        if vars.youtube_api == None:
            stalkChannel.update_youtube_api(0)
        video_type = "unknown"
        if "/shorts/" in video_link:
            video_type = "reels"
        elif "/watch?v=" in video_link:
            video_type = "normal"
        all_comments = []
        total_comments = "undefined"
        if video_type == "reels":
            if open_reels == True:
                vars.webdriver.get(video_link)
                time.sleep(1)
                try:
                    total_comments = vars.webdriver.find_element(by = By.XPATH, value = f"/html/body/div/div[3]/shorts-page/shorts-carousel/div/div/div[3]/shorts-video/div/div[3]/ytm-reel-player-overlay-renderer/div[1]/div[2]/c3-material-button[1]/button/div/div").text
                except:
                    total_comments = vars.webdriver.find_element(by = By.XPATH, value = f"/html/body/div/div[3]/shorts-page/shorts-carousel/div/div/div[1]/shorts-video/div/div[3]/ytm-reel-player-overlay-renderer/div[1]/div[2]/c3-material-button[1]/button/div/div").text
                if total_comments == "Compartilhar":
                    total_comments = "Desativado"
                print(f"VÍDEO DO TIPO 'REELS' COM TOTAL DE '{total_comments}' COMENTÁRIOS!\n")
            else:
                print(f"VÍDEO DO TIPO 'REELS', O SOFTWARE ESTÁ CONFIGURADO PARA NÃO PEGAR OS COMENTÁRIOS!\n")
        elif video_type == "normal":
            try:
                total_comments = 0
                video_id = video_link.split("/watch?v=")[1].split("&")[0]
                video_resource = vars.youtube_api.commentThreads().list(part = "snippet,replies", maxResults = max_comments, videoId = video_id, textFormat = "plainText").execute()
                new_amount_comments, new_comments = stalkChannel.filter_video_comments_from_api(video_resource)
                total_comments += new_amount_comments
                for i in new_comments:
                    all_comments.append(i)
                    if len(all_comments) >= max_comments and exact_value == True:
                        break
                    #print(f"{len(all_comments) + 1}")
                if len(all_comments) < max_comments:
                    while True:
                        params = {
                            'key': vars.API_KEY_IN_USE,
                            'part': 'snippet,replies',
                            'videoId': video_id,
                            'textFormat': 'plaintext',
                            'maxResults': max_comments
                        }
                        if "nextPageToken" in video_resource.keys():
                            params['pageToken'] = video_resource['nextPageToken']
                        else:
                            break
                        video_response = requests.get(f"{vars.API_URL}commentThreads", params = params)
                        video_resource = video_response.json()
                        new_amount_comments, new_comments = stalkChannel.filter_video_comments_from_api(video_resource)
                        total_comments += new_amount_comments
                        for i in new_comments:
                            all_comments.append(i)
                            if len(all_comments) >= max_comments and exact_value == True:
                                break
                            #print(f"{len(all_comments) + 1}")
                        if len(all_comments) >= max_comments:
                            break
                        if "nextPageToken" in video_resource.keys():
                            pass
                        else:
                            break
                print(f"VÍDEO DO TIPO 'NORMAL' COM TOTAL DE '{len(all_comments)}' COMENTÁRIOS OBTIDOS!\n")
            except Exception as e:
                if "quota" in str(e):
                    stalkChannel.next_youtube_api()
                    return stalkChannel.get_all_comments_from_video(video_link, open_reels, max_comments, exact_value)
                #error_details(str(traceback.format_exc()), str(e))
                print("VÍDEO DO TIPO 'NORMAL', COM COMENTÁRIOS DESATIVADOS!\n")
        else:
            video_type = "undefined"
            print(f"VÍDEO DO TIPO 'UNDEFINED'!\n")
        return video_type, all_comments, total_comments




    #carrega comentarios de um vídeo do youtube usando a api do youtube
    def filter_video_comments_from_api(match):
        total_comments = 0
        all_comments = []
        for comment in match['items']:
            new_comment = {'user':comment['snippet']['topLevelComment']['snippet']['authorDisplayName'], 'user_channel':comment['snippet']['topLevelComment']['snippet']['authorChannelUrl'], 'comment':comment['snippet']['topLevelComment']['snippet']['textDisplay']}
            replies = []
            if "replies" in comment.keys():
                for reply in comment['replies']['comments']: #os primeiros são os últimos
                    new_reply = {'user':reply['snippet']['authorDisplayName'], 'user_channel':reply['snippet']['authorChannelUrl'] , 'comment':reply['snippet']['textDisplay']}
                    replies.append(new_reply)
                replies.reverse()
            total_comments += 1 + len(replies)
            new_comment["replies"] = replies
            all_comments.append(new_comment)
        return total_comments, all_comments




    #filtra os comentários pelo nome ou link do canal de quem comentou
    def search_for_target_in_comments(comments, target_name, target_channel_link, by_user = True, by_channel_link = True, return_amount = False):
        filtered_comments = []
        amount_comments = 0
        for comment in comments:
            amount_comments += 1
            if (target_name in comment['user'] and by_user == True) or (target_channel_link.split("/channel/")[1] in comment['user_channel'] and by_channel_link == True):
                filtered_comments.append(comment)
            else:
                for reply in comment['replies']:
                    amount_comments += 1
                    if (target_name in reply['user'] and by_user == True)  or (target_channel_link.split("/channel/")[1] in reply['user_channel'] and by_channel_link == True) or (target_name in reply['comment'] and by_user == True):
                        filtered_comments.append(comment)
                        break
        if return_amount == True:
            return amount_comments, filtered_comments
        else:
            return filtered_comments




    #pega todos os comentários do canal alvo em todos os canais que ele é inscrito
    def get_all_comments_from_target(target_channel_link, start_index = 0, max_comments_per_video = 1000):
        target_name, followed_channels = stalkChannel.get_followed_channels_of_target(target_channel_link)
        all_comments_amount,total_filtered_comments = stalkChannel.itterate_over_all_saved_comments_to_find_target(target_name, target_channel_link, start_index)
        print("----------------------------------------------------------------------")
        print(f"INSCRITO EM '{len(followed_channels)}' CANAIS!")
        print(f"NESTE PONTO JÁ FORAM SALVOS '{all_comments_amount}' COMENTÁRIOS, DOS QUAIS '{total_filtered_comments}' FORAM FILTRADOS!")
        for channel_index, channel_link in enumerate(followed_channels):
            if channel_index < start_index:
                    continue
            print("----------------------------------------------------------------------")
            new_channel = {}
            print(f"PESQUISANDO NO CANAL '{channel_index + 1}/{len(followed_channels)}' (index = '{channel_index}', link = '{channel_link}')!\n")
            channel_name, channel_videos = stalkChannel.get_all_videos_from_channel(channel_link)
            print(f"\nNOME DO CANAL É '{channel_name}'!")
            print(f"TOTAL DE {len(channel_videos)} VÍDEOS!\n")
            new_channel["name"] = channel_name
            new_channel["link"] = channel_link
            new_channel["videos"] = {}
            for video_index, video in enumerate(channel_videos):
                print(f"PESQUISANDO COMENTÁRIOS DO VÍDEO '{video_index + 1}/{len(channel_videos)}' (link = '{video['link']}')!")
                new_channel["videos"][video_index + 1] = {}
                new_channel["videos"][video_index + 1]["title"] = video["title"]
                new_channel["videos"][video_index + 1]["link"] = video["link"]
                new_channel["videos"][video_index + 1]["age"] = video["age"]
                video_type, all_comments, total_comments = stalkChannel.get_all_comments_from_video(video_link = video["link"], max_comments = max_comments_per_video, )
                try:
                    all_comments_amount += int(total_comments)
                except:
                    pass
                new_channel["videos"][video_index + 1]["type"] = video_type
                new_channel["videos"][video_index + 1]["all_comments"] = all_comments
                amount_comments, filtered_comments = stalkChannel.search_for_target_in_comments(all_comments, target_name, target_channel_link, return_amount = True)
                all_comments_amount += amount_comments
                for i in filtered_comments:
                    total_filtered_comments += 1
            print(f"TOTAL DE '{all_comments_amount}' COMENTÁRIOS LIDOS ATÉ AGORA!")
            print(f"TOTAL DE '{total_filtered_comments}' COMENTÁRIOS FILTRADOS ATÉ AGORA!")
            with open(f"info/txt/{channel_index + 1}-channel.txt", "w+") as f:
                f.write(json.dumps(new_channel))
            with open(f"info/pickle/{channel_index + 1}-channel.pickle", "wb") as f:
                pickle.dump(new_channel, f, protocol = pickle.HIGHEST_PROTOCOL)
        print("----------------------------------------------------------------------")
        print(filtered_comments)
        print("FINISH")




    #carrega todos os arquivos gerados como dicionario
    def load_archives():
        info_channels = {'channels':{}}
        archives = os.listdir(path = "info/pickle/")
        for archive in archives:
            with open(f"info/pickle/{archive}", "rb") as f:
                new_channel = pickle.load(f)
                info_channels['channels'][new_channel['name']] = new_channel
        return info_channels




    #ittera entre todos os comentarios dos arquivos salvos
    def itterate_over_all_saved_comments_to_find_target(target_name, target_channel_link, until_channel_index = 1000):
        info_channels = stalkChannel.load_archives()
        total_filtered_comments = 0
        total_comments = 0
        # print(info_channels['channels'].keys())
        for channel_index, i in enumerate(info_channels['channels'].values()):
            if channel_index == until_channel_index:
                break
            for j in i['videos'].values():
                #title, link ,age, type, all_comments, filtered_comments
                amount_comments, filtered_comments = stalkChannel.search_for_target_in_comments(j['all_comments'], target_name, target_channel_link, return_amount = True)
                total_comments += amount_comments
                for k in filtered_comments:
                    total_filtered_comments += 1
                    print(f"{total_filtered_comments} = '{k}' at video link '{j['link']}'!")
        print(f"FOI FILTRADO UM TOTAL DE '{total_comments}' COMENTÁRIOS!")
        return total_comments, total_filtered_comments
