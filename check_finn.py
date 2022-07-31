from urllib.request import urlopen
from bs4 import BeautifulSoup

# url = "http://olympus.realpython.org/profiles/aphrodite"
# url = "https://www.finn.no/boat/forsale/search.html?class=2186&length_feet_from=9&length_feet_to=10&location=20016&sort=PUBLISHED_DESC"
# url = "https://www.finn.no/boat/forsale/search.html?class=2186&length_feet_from=9&length_feet_to=10&location=20016&published=1&sort=PUBLISHED_DESC"


class SheilaJob:
    def __init__(self):
        self.seenLinks = []
        self.url = "https://www.finn.no/job/fulltime/search.html?industry=1&industry=14&industry=3&industry=51&industry=53&lat=63.39188178422313&location=2.20001.20016.20318&lon=10.436492112530033&published=1&radius=7000&sort=RELEVANCE"

    def get_new_articles(self):
        page = urlopen(self.url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        result_set = soup.find_all("a", attrs={"class":"ads__unit__link"})
        new_results = []
        for article in result_set:
            link = str(article).split(" ")[2][6:-1]
            if link not in self.seenLinks:
                self.seenLinks.append(link)
                new_results.append(link)
        
        return new_results


if __name__ == "__main__":
    sheila_job = SheilaJob()
    print(sheila_job.get_new_articles())


"""
<article class="ads__unit">
    <div aria-owns="ads__unit__content__title262375410"></div>
    <div class="ads__unit__img">
        <div class="ads__unit__img__ratio img-format img-format--ratio3by2 img-format--centered img-format--logo">
            <img alt="" class="img-format__img" loading="lazy" src="https://images.finncdn.no/dynamic/320w/2022/6/vertical-0/16/0/262/375/410_1831778707.jpg"/>
            
        </div>
    </div>
    <div class="ads__unit__content">
        <h2 class="ads__unit__content__title ads__unit__content__title--fav-placeholder" id="ads__unit__content__title262375410">
            <a class="ads__unit__link" href="https://www.finn.no/job/fulltime/ad.html?finnkode=262375410" id="262375410">Trøndelag fylkeskontor søker rådgiver i 100% fast stilling</a>
        </h2>
        <div class="ads__unit__content__status u-position-relative">
            <div class="u-position-absolute u-top u-right" style="z-index:2"></div>
        </div>
        <div class="ads__unit__content__details">
            <div class="u-stone">Ny i dag | Trondheim</div>
        </div>
        <div class="ads__unit__content__keys">
            <div>Rådgiver</div>
        </div>
        <div>
            <div class="u-float-left"><div class="ads__unit__content__list">Norsk Sykepleierforbund</div>
            <div class="ads__unit__content__list">1 stilling</div>
    </div>
    </div>
    </div>
</article>
"""