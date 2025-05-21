class LanguageDetector:
    def __init__(self):
        # Добавление списока ключевых слов для каждого языка
        self.keywords = {
            'ru': ['aвторизация', 'войти', 'пароль'],
            'en': ['authorization', 'login', 'password']
        }

    def get_lang(self, text):
        text_lower = text.lower()
        # Подсчет совпадений ключевых слов
        ru_matches = sum(word in text_lower for word in self.keywords['ru'])
        en_matches = sum(word in text_lower for word in self.keywords['en'])
        if ru_matches > en_matches:
            return 'ru'
        elif en_matches > ru_matches:
            return 'en'
        else:
            return 'unknown'


class Localization:
    def __init__(self, lang='ru'):
        self.lang = lang
        self.translations = {
            'ru': {
                'devices': 'Устройства',
            },
            'en': {
                'devices': 'Devices',
            },
            'unknown': {

            }
        }

    def get(self, key):
        return self.translations[self.lang].get(key, key)

    def set_lang(self, lang):
        self.lang = lang
