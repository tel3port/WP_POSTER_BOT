import csv
import re
import time
import traceback
from collections import Counter
from random import randint
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import globals as gls


class WP_Auto_Bot:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-sgm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--headless")
        # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        self.driver = webdriver.Chrome("./chromedriver", options=chrome_options)

    @staticmethod
    def external_link_extractor(sent_site):
        site = sent_site.split('//')[1]
        print(f"extracting external links on this list: {site}")

        base_url_list = [
            f'https://afflat3d1.com/lnk.asp?o=9075&c=918277&a=242672&k=EBF2EDB942180C1F39AC57CE3994F57C&l=8504&s1={site}',
            f'https://afflat3d1.com/lnk.asp?o=18084&c=918277&a=242672&k=580FAC50554E1E3F5AACC583D06DE0AD&l=19332&s1={site}',
            f'https://afflat3d1.com/lnk.asp?o=18099&c=918277&a=242672&k=89F4A996358DADE546AA2BF166C9A7F9&l=19340&s1={site}',
            f'https://afflat3d1.com/lnk.asp?o=18095&c=918277&a=242672&k=C12104E1F23E5C340EAF089395EBD125&l=19345&s1={site}',
            f'https://afflat3d1.com/lnk.asp?o=18627&c=918277&a=242672&k=B97D03D349CE4FE1BE27D635A16AD24B&l=19818&s1={site}',
            f'https://afflat3d1.com/lnk.asp?o=19322&c=918277&a=242672&k=F5A185D25CB8289CD91DF3803D395C64&l=20323&s1={site}',
            f'https://afflat3d1.com/lnk.asp?o=19594&c=918277&a=242672&k=30F2E776196A860C8FE3BBDE6D69D334&l=20556&s1={site}',
            f'https://afflat3d1.com/lnk.asp?o=7527&c=918277&a=242672&k=956D04E486409DA8ED5528F3448FB86F&l=6239&s1={site}',
            f'https://afflat3d1.com/lnk.asp?o=10721&c=918277&a=242672&k=18DBF0EF0820E9FDB52660B31C464213&l=10603&s1={site}',
            f'https://afflat3d1.com/lnk.asp?o=18174&c=918277&a=242672&k=29DA121E59E0456E7F1B9D705D276327&l=19429&s1={site}',
        ]
        extracted_external_links = []
        extracted_external_links.extend(base_url_list)

        return extracted_external_links

    @staticmethod
    def credentials_getter():
        my_base_urls = []

        my_keywords = []
        with open('dict/credentials_wp_poster_bot.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 0:
                    my_base_urls.append(row[0])
                    my_keywords.append(row[1])

        return my_base_urls, my_keywords

    def wp_login(self):
        wp_login_url = 'https://wordpress.com/wp-login.php?checkemail=confirm'
        wp_email_xpath = '//*[@id="user_login"]'
        wp_password_xpath = '//*[@id="user_pass"]'
        wp_login_xpath = '//*[@id="wp-submit"]'
        wp_email = "kensymr@aol.com"
        wp_password = '7zDFacxf&VXba^nCC53FXWCCAh9'

        try:
            self.driver.delete_all_cookies()
            self.driver.get(wp_login_url)
            gls.sleep_time()
            self.driver.find_element_by_xpath(wp_email_xpath).send_keys(wp_email)
            gls.sleep_time()
            self.driver.find_element_by_xpath(wp_password_xpath).send_keys(wp_password)
            gls.sleep_time()
            continue_btn = self.driver.find_element_by_xpath(wp_login_xpath)
            gls.sleep_time()
            continue_btn.click()

        except Exception as ex:
            print("wp login error at ", ex)
            print(traceback.format_exc())

    def prl_article_extractor_and_saver(self, base_url, username, password, keyword_string, keyword_list, external_link_list):
        print("logging in at killerplr...")
        print("session id at login: ", self.driver.session_id)

        while 1:
            try:
                self.driver.get(f"{base_url}/access/login")
                WebDriverWait(self.driver, 25).until(EC.element_to_be_clickable((By.NAME, "log")))

                # fill up the credential fields
                self.driver.find_element_by_name('log').send_keys(username)
                time.sleep(5)
                self.driver.find_element_by_name('pwd').send_keys(password)
                time.sleep(5)

                self.driver.find_element_by_xpath('//*[contains(@name,"wp-submit")]').click()
                time.sleep(5)
                print("login success...")
                break

            except Exception as e:
                print(f"the login issue at {base_url}/access/login is: ", e)
                print(traceback.format_exc())
                time.sleep(20)
                pass

        print("starting prl extraction")
        try:
            my_url = f'{base_url}/categories/'

            self.driver.get(my_url)
            data = self.driver.page_source
            soup = BeautifulSoup(data, "html.parser")
            links_classes = soup.find_all('div', class_="main-category")

            category_list = []  # houses all category links
            for link_class in links_classes:

                links = link_class.find_all('a', href=True)

                for a in links:
                    category_list.append(a['href'])

            for _ in range(2):

                random_category_link = category_list[randint(0, len(category_list) - 1)]
                print(f"extracting on cat: {random_category_link}")
                opt_random_category_link = f'{random_category_link}/page/{randint(2, 5)}'
                self.driver.get(opt_random_category_link)
                data = self.driver.page_source
                soup = BeautifulSoup(data, "html.parser")
                article_links_classes = soup.find_all('h2', class_="entry-title")

                article_page_links = []  # houses all article pages

                for art_class in article_links_classes:
                    article_page_links.append(art_class.a['href'])

                # start extracting articles

                for single_page_link in article_page_links:
                    self.driver.get(single_page_link)
                    data = self.driver.page_source
                    soup = BeautifulSoup(data, "html.parser")
                    heading = soup.find("h1", class_="entry-title")
                    print(f'killerplrarticles HEADING: {heading.text}')
                    content = soup.find('div', class_="entry-content")

                    # TODO optimise here
                    opt_heading, opt_content = self.prl_content_optimiser(heading.text, content.text, keyword_string,keyword_list, external_link_list)

                    with open('dict/final_articles_wp_poster_bot.csv', 'a', newline='') as file:
                        fieldnames = ['heading', 'content']
                        writer = csv.DictWriter(file, fieldnames=fieldnames)

                        writer.writerow({'heading': opt_heading, 'content': opt_content})

        except Exception as em:
            print('prl_extractor Error occurred ' + str(em))
            print(traceback.format_exc())
            pass

        finally:
            print(" prl_extractor() done")

    @staticmethod
    def prl_content_optimiser(title, content, my_kw_str, my_keyword_list, my_external_links):
        print(f"kw string: {my_kw_str}")
        random_kword = my_keyword_list[randint(0, len(my_keyword_list) - 1)]

        opt_title = title.replace(title[:title.index(' ')], random_kword, 1)  # replace first word with keyword
        opt_kw_str = f'<article> <h3>{opt_title}</h3> <p>{content}</p> </article>'
        opt_content_0 = content.lower()
        opt_content_1 = opt_content_0.replace('.', ". \n")
        words = re.findall(r'\w+', opt_content_1)
        cap_words = [word.upper() for word in words]
        word_counts = Counter(cap_words)
        list1 = word_counts.most_common(10)
        most_common_dict = dict(tuple(list1))
        most_common_keys = list(most_common_dict.keys())
        final_words = []
        for s_word in most_common_keys:
            if len(s_word) > 3:
                final_words.append(s_word.lower())

        opt_content2_chars = opt_content_1.split(' ')
        opt_content_3 = ''
        print("final list of most words: ", final_words)
        # replaces self.keyword_list and internal links
        count = 0
        for word in opt_content2_chars:

            if word in final_words:
                random_kw = my_keyword_list[randint(0, len(my_keyword_list) - 1)]
                random_external_link = my_external_links[randint(0, len(my_external_links) - 1)]
                replacement = f' <a href={random_external_link}>{random_kw}  </a> '
                opt_content_3 += replacement + " "
            else:
                opt_content_3 += word + " "
            count += 1

        return opt_title, f'{opt_content_3}.'

    @staticmethod
    def optimised_article_getter():
        ai_headings = []
        ai_articles = []

        with open('dict/final_articles_wp_poster_bot.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 0:
                    ai_headings.append(row[0])
                    ai_articles.append(row[1])

        return ai_headings, ai_articles

    def wp_post(self, title, post, site, kw_list):
        wp_post_url = f'{site}/wp-admin/post-new.php'
        wp_title_xpath = '//*[@id="post-title-1"]'
        wp_post_xpath = '//*[@id="post-content-0"]'
        wp_publish_1_xpath = '//button[text()="Publish"]'
        code_editor_xpath = "//button[contains(.,'Code editor')]"
        prepub_checkbox_xpath = '//*[@id="inspector-checkbox-control-2"]'
        close_panel_xpath = '//*[@aria-label="Close panel"]'
        drop_down_xpath = '//*[@aria-label="More tools & options"]'
        tags_xpath = "//button[contains(.,'Tags')]"
        tags_input_xpath = '//*[@id="components-form-token-input-0"]'

        print(f'kw list {kw_list}')

        try:
            self.driver.get(wp_post_url)
            time.sleep(10)
            self.driver.find_element_by_xpath(drop_down_xpath).click()
            gls.sleep_time()
            self.driver.find_element_by_xpath(code_editor_xpath).click()
            gls.sleep_time()
            self.driver.find_element_by_xpath(drop_down_xpath).click()
            gls.sleep_time()
            self.driver.find_element_by_xpath(wp_title_xpath).click()
            gls.sleep_time()
            self.driver.find_element_by_xpath(wp_title_xpath).send_keys(title)
            gls.sleep_time()
            self.driver.find_element_by_xpath(wp_post_xpath).click()
            gls.sleep_time()
            self.driver.find_element_by_xpath(wp_post_xpath).send_keys(post)
            gls.sleep_time()
            self.driver.find_element_by_xpath(tags_xpath).click()
            gls.sleep_time()
            self.driver.find_element_by_xpath(tags_input_xpath).send_keys(kw_list)
            gls.sleep_time()
            pub1_btn = self.driver.find_element_by_xpath(wp_publish_1_xpath)
            gls.sleep_time()
            pub1_btn.click()
            gls.sleep_time()
            prepub_checkbox = self.driver.find_element_by_xpath(prepub_checkbox_xpath)
            if prepub_checkbox.is_selected():
                prepub_checkbox.click()
            gls.sleep_time()
            close_btn = self.driver.find_element_by_xpath(close_panel_xpath)
            gls.sleep_time()
            close_btn.click()
            gls.sleep_time()
            pub1_btn.click()
            time.sleep(15)

        except Exception as ex:
            print("wp post error at ", ex)
            print(traceback.format_exc())

        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
            alert = self.driver.switch_to.alert()
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")

    def clean_up(self):
        self.driver.delete_all_cookies()
        open('dict/final_articles_wp_poster_bot.csv', 'w').close()


if __name__ == "__main__":
    loop_count_num = 0

    while 1:
        try:
            print(f"MAIN LOOP COUNT NUM {loop_count_num}")

            autobot = WP_Auto_Bot()
            urls = autobot.credentials_getter()[0]
            keywords = autobot.credentials_getter()[1]

            my_cred_size = len(urls)

            random_account_num = randint(0, my_cred_size)  # get a random account row
            account_url = urls[random_account_num]
            account_kws = keywords[random_account_num]

            external_links = autobot.external_link_extractor(account_url.strip())
            autobot.prl_article_extractor_and_saver('https://www.killerplrarticles.com', '2ksaber@gmail.com', '2ksaber@gmail.com', account_kws, account_kws.split(','), external_links)

            headings, articles = autobot.optimised_article_getter()

            articles_num = len(headings)

            autobot.wp_login()
            for ix in range(articles_num):

                autobot.wp_post(headings[ix], articles[ix], account_url, account_kws)

            autobot.clean_up()

            loop_count_num += 1

        except Exception as em:

            print('main loop Error occurred ' + str(em))

            print(traceback.format_exc())


print("broke out of the script")
# todo create multiple wp accounts
# todo upload to aws and deploy
