from selenium.webdriver.common.by import By
import time
import math

def count_playlist_time(driver, link):
    total_time = 0
    driver.get(link)
    time.sleep(1)
    playlist_lenght = int(driver.find_element(by = By.XPATH, value = f"/html/body/ytm-app/div[1]/ytm-watch/ytm-single-column-watch-next-results-renderer/ytm-playlist/ytm-playlist-panel-header/div/div").text.split("/")[1].split(" ")[1])
    for id in range(playlist_lenght):
        video_time = driver.find_element(by = By.XPATH, value = f"/html/body/ytm-app/div[1]/ytm-watch/ytm-single-column-watch-next-results-renderer/ytm-playlist/div/div/lazy-list/ytm-playlist-panel-video-renderer[{id + 1}]/div/a/div/div[2]/ytm-thumbnail-overlay-time-status-renderer/span").text
        readble_video_time = video_time.split(":")
        if len(readble_video_time) == 3:
            time_to_add = int(readble_video_time[0])*3600 + int(readble_video_time[1])*60 + int(readble_video_time[2])
        else:
            time_to_add = int(readble_video_time[0])*60 + int(readble_video_time[1])
        total_time += time_to_add
        print(f"{id + 1}/{playlist_lenght} = total de {time_to_add} segundos", end = "")
        hours_to_add = math.floor(time_to_add/3600)
        time_to_add -= hours_to_add*3600
        minutes_to_add = math.floor(time_to_add/60)
        time_to_add -= minutes_to_add*60
        print(f", ou {hours_to_add} horas, {minutes_to_add} minutos e {time_to_add} segundos!")
    total_hours = math.floor(total_time/3600)
    total_time -= total_hours*3600
    total_minutes = math.floor(total_time/60)
    total_time -= total_minutes*60
    print(f"tempo total da playlist é {total_hours} horas, {total_minutes} minutos e {total_time} segundos!")
