from time import sleep
from configparser import ConfigParser

from selenium import webdriver


class ConfigParams(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)
        self.config = ConfigParser()
        self.config.read('files\\config.ini')

    def get_option(self, section, option):
        return self.config[section][option]


class SeleniumTask:
    def __init__(self, url):
        self.driver = webdriver.Chrome(executable_path='files\\chromedriver.exe')
        self.driver.maximize_window()
        self.open_url(url)

    def open_url(self, url):
        self.driver.get(url)

    def select_country(self, country):
        self.driver.find_element_by_xpath('//dd[@id="country-element"]').click()  # Выпадающий список государств
        self.driver.find_element_by_xpath(f'//span[@data-value="{country}"]').click()  # Country

    def select_language(self, language_code):
        self.driver.find_element_by_xpath('//div[@id="language"]').click()  # Выпадающий список языков
        self.driver.find_element_by_xpath(f'//label[@for="{language_code}"]').click()  # Выбираем язык
        self.driver.find_element_by_xpath(f'//a[@class="selecter-fieldset-submit"]').click()  # Apply

    def job_counter(self):
        job_text = self.driver.find_element_by_xpath('//h3[@class="pb15-sm-down mb30-md-up text-center-md-down"]')
        return job_text.text.split(' ', 1)[0]

    def close_session(self):
        self.driver.close()


def result_text(*args):
    with open('files\\result_qa_task.txt', 'a') as f:
        result = ' '.join(args) + '\n'
        f.writelines(result)


def main():
    config = ConfigParams()
    country = config.get_option('Country', 'romania')  # Стартовый параметр для государства
    language = config.get_option('Language', 'english')  # Стартовый параметр для языка

    qa_task = SeleniumTask('https://careers.veeam.com/')
    qa_task.select_country(country)  # параметризуем Государство
    qa_task.select_language(language)  # параметризуем код языка
    sleep(3)  # Чтоб успел браузер отработать пауза в 3 сек
    job_counter = qa_task.job_counter()  # Количество вакансий
    print('Количество выданных вакансий:', job_counter, sep=' ')  # результат в консоль
    result_text(country, language, f'Количество выданных вакансий: {job_counter}')  # запись в текстовый файл
    qa_task.close_session()


if __name__ == '__main__':
    main()