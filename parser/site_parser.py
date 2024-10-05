import requests
from bs4 import BeautifulSoup

links = [
    "https://eora.ru/cases/promyshlennaya-bezopasnost",
    "https://eora.ru/cases/lamoda-systema-segmentacii-i-poiska-po-pohozhey-odezhde",
    "https://eora.ru/cases/navyki-dlya-golosovyh-assistentov/karas-golosovoy-assistent",
    "https://eora.ru/cases/assistenty-dlya-gorodov",
    "https://eora.ru/cases/avtomatizaciya-v-promyshlennosti/chemrar-raspoznovanie-molekul",
    "https://eora.ru/cases/zeptolab-skazki-pro-amnyama-dlya-sberbox",
    "https://eora.ru/cases/goosegaming-algoritm-dlya-ocenki-igrokov",
    "https://eora.ru/cases/dodo-pizza-robot-analitik-otzyvov",
    "https://eora.ru/cases/ifarm-nejroset-dlya-ferm",
    "https://eora.ru/cases/zhivibezstraha-navyk-dlya-proverki-rodinok",
    "https://eora.ru/cases/sportrecs-nejroset-operator-sportivnyh-translyacij",
    "https://eora.ru/cases/avon-chat-bot-dlya-zhenshchin",
    "https://eora.ru/cases/navyki-dlya-golosovyh-assistentov/navyk-dlya-proverki-loterejnyh-biletov",
    "https://eora.ru/cases/computer-vision/iss-analiz-foto-avtomobilej",
    "https://eora.ru/cases/purina-master-bot",
    "https://eora.ru/cases/skinclub-algoritm-dlya-ocenki-veroyatnostej",
    "https://eora.ru/cases/skolkovo-chat-bot-dlya-startapov-i-investorov",
    "https://eora.ru/cases/purina-podbor-korma-dlya-sobaki",
    "https://eora.ru/cases/purina-navyk-viktorina",
    "https://eora.ru/cases/dodo-pizza-pilot-po-avtomatizacii-kontakt-centra",
    "https://eora.ru/cases/dodo-pizza-avtomatizaciya-kontakt-centra",
    "https://eora.ru/cases/icl-bot-sufler-dlya-kontakt-centra",
    "https://eora.ru/cases/s7-navyk-dlya-podbora-aviabiletov",
    "https://eora.ru/cases/workeat-whatsapp-bot",
    "https://eora.ru/cases/absolyut-strahovanie-navyk-dlya-raschyota-strahovki",
    "https://eora.ru/cases/kazanexpress-poisk-tovarov-po-foto",
    "https://eora.ru/cases/kazanexpress-sistema-rekomendacij-na-sajte",
    "https://eora.ru/cases/intels-proverka-logotipa-na-plagiat",
    "https://eora.ru/cases/karcher-viktorina-s-voprosami-pro-uborku",
    "https://eora.ru/cases/chat-boty/purina-friskies-chat-bot-na-sajte",
    "https://eora.ru/cases/nejroset-segmentaciya-video",
    "https://eora.ru/cases/chat-boty/essa-nejroset-dlya-generacii-rolikov",
    "https://eora.ru/cases/qiwi-poisk-anomalij",
]


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def parse_sites(links):
    for index, link in enumerate(links):
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1').text if soup.find('h1') else "No title"
            divs = soup.find_all('div', class_='tn-atom')

            content = [div.text.strip() for div in divs if div.text.strip()]

            filename = f"project_{index + 1}.txt"

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"URL: {link}\n")
                file.write(f"Title: {title}\n\n")
                file.write("Content:\n")
                file.write("\n".join(content))

            print(f"Data saved to {filename}")
        else:
            print(f"Failed to retrieve {link}: Status code {response.status_code}")


if __name__ == "__main__":
    parse_sites(links)
