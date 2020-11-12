from bs4 import BeautifulSoup
import requests


# graph search problem

# expects url in form /wiki/someTextHere
def is_valid_url(url):
    # print("url: " + url + "\nurl[:6]: " + url[:6])
    return url is not None and len(url) > 6 and url[0] != "#" and url[:6] == "/wiki/"


def crawl(next_link):
    next_link = "/wiki/" + next_link
    visited_links = []

    # if title is not form /wiki/validTitle break
    if not is_valid_url(next_link):
        print("Invalid title: " + next_link)
        exit()

    while True:
        next_link = "https://en.wikipedia.org" + next_link
        res = requests.get(next_link)
        content = res.content

        soup = BeautifulSoup(content, 'html.parser')
        # get the title from current header
        title = soup.find(id="firstHeading")
        # print(title)

        print(title.string)
        if title.string == "Philosophy":
            print("You crawled through {} pages to Philosophy!\n".format(len(visited_links)))
            return

        paragraphs = soup.find(id="bodyContent").findAll("p")
        # paragraphs = content.findAll('p')

        found_next_url = False
        for p in paragraphs:
            if not found_next_url:
                parenthesis = False
                for text in p.contents:
                    if not found_next_url:
                        # print("Text line 62: " + str(text))
                        if "(" in text:
                            parenthesis = True
                        if ")" in text and parenthesis:
                            parenthesis = False

                        if not parenthesis:
                            if not isinstance(text, str):
                                try:
                                    link = text['href']
                                    # print("X: " + x)
                                    if link not in visited_links and "." not in link:
                                        found_next_url = True
                                        # print(x)
                                        next_link = link
                                        visited_links.append(next_link)
                                except:
                                    pass


while True:
    wiki_link = input("Enter wiki title to crawl from (e.g. to crawl from "
                      "\"https://en.wikipedia.org/wiki/Fizz_buzz\", enter \"Fizz_Buzz\"."
                      "\nIf you would like to exit the program, type \"EXIT\" (case sensitive): \n")
    if input == "EXIT" or input == "\"EXIT\"":
        break
    crawl(wiki_link)
