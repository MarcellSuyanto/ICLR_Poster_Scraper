from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.webdriver.chrome.options import Options


title_links = {
    #'llm': 'https://iclr2025.vizhub.ai/?brushed=%255B%255B413.3249816894531%252C-5.2112884521484375%255D%252C%255B757.7249755859375%252C379.1637268066406%255D%255D',
    'speech': 'https://iclr2025.vizhub.ai/?brushed=%255B%255B339.5250244140625%252C46.03871154785156%255D%252C%255B429.72503662109375%252C108.56371307373047%255D%255D',
    'multimodal_models': 'https://iclr2025.vizhub.ai/?brushed=%255B%255B179.62503051757812%252C18.363710403442383%255D%252C%255B330.3000183105469%252C234.6387176513672%255D%255D',
    'agents': 'https://iclr2025.vizhub.ai/?brushed=%255B%255B678.7999877929688%252C210.03871154785156%255D%252C%255B750.5499877929688%252C383.2637023925781%255D%255D',
    'reinforcement_learning_and_robots': 'https://iclr2025.vizhub.ai/?brushed=%255B%255B596.7999877929688%252C426.313720703125%255D%252C%255B791.5499877929688%252C658.9887084960938%255D%255D',
    'federated': 'https://iclr2025.vizhub.ai/?brushed=%255B%255B482%252C424.2637023925781%255D%252C%255B544.5250244140625%252C528.813720703125%255D%255D',
    'graph': 'https://iclr2025.vizhub.ai/?brushed=%255B%255B293.3999938964844%252C666.1636962890625%255D%252C%255B415.375%252C804.875%255D%255D',
    'drug_and_molecules': 'https://iclr2025.vizhub.ai/?brushed=%255B%255B165.2750244140625%252C646.688720703125%255D%252C%255B296.47503662109375%252C787.1137084960938%255D%255D',
    'time_series': 'https://iclr2025.vizhub.ai/?brushed=%255B%255B252.39999389648438%252C422.2137145996094%255D%252C%255B337.4750061035156%252C532.9136962890625%255D%255D',
    'diffusion_models': 'https://iclr2025.vizhub.ai/?brushed=%255B%255B-0.7749814987182617%252C296.1387023925781%255D%252C%255B261.6250305175781%252C673.3386840820312%255D%255D',
    '3D_and_gaussian_splatting': 'https://iclr2025.vizhub.ai/?brushed=%255B%255B-2.824981689453125%252C187.48870849609375%255D%252C%255B199.1000213623047%252C388.3887023925781%255D%255D',
}

def initialize_driver(title):
    download_dir = f"C:\\Users\\Marcell Suyanto\\Dropbox\\Coding\\Python\\ICLR_scrape\\{title}"
    chrome_options = Options()
    prefs = {
        "download.default_directory": download_dir,
        "plugins.always_open_pdf_externally": True, 
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(5)
    return (driver, download_dir)

def get_papers(driver, title, download_dir):
    link = title_links[title]
    driver.get(link)
    time.sleep(5)
    main_window = driver.current_window_handle

    papers = driver.find_elements(By.XPATH, "//div[@class='paper svelte-ki60ov']")
    actions = ActionChains(driver)
    for paper in papers:
        actions.key_down(Keys.ALT).click(paper).key_up(Keys.ALT).perform()
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != main_window:
                driver.switch_to.window(window_handle)
                break
        tab_link = driver.current_url
        pdf_id = tab_link.split('?')[-1]
        pdf_link = 'https://openreview.net/pdf?' + pdf_id
        print("PDF Link:", pdf_link)
        driver.get(pdf_link)
        def wait_for_download(directory):
            dl_wait = True
            while dl_wait:
                time.sleep(1)
                dl_wait = False
                for fname in os.listdir(directory):
                    if fname.endswith(".crdownload"):
                        dl_wait = True
            return not dl_wait

        finished = wait_for_download(download_dir)
        driver.close()
        driver.switch_to.window(main_window)

for title in title_links.keys():
    driver, download_dir = initialize_driver(title)
    get_papers(driver, title, download_dir)
    driver.quit()
