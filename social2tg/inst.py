import instaloader
import time

import CONFIG
from .common import Image, Post, RequestsSource, SeleniumSource, Source, Video
from .utils import find_elem, get_logger, ip_in_string


logger = get_logger()


class InstagramSource(Source):
    """
    Base for any Instagram clients, and common Instgram logic
    """
    def get_last_posts(self):
        """
        Get list of Post instances of posts
        which appeared after the last check
        """
        raise NotImplementedError


class InstagramPost(Post):

    def construct_footer(self):
        footer = (
            f'\n\n<i><a href="{self.orig_url}">{self.update_type.title()}</a> by '
            f'<a href="https://www.instagram.com/{self.author[1:]}">{self.author}</a></i>'
        )
        return footer


class GramhirPost(InstagramPost):
    """
    Post handler for Gramhir source
    """
    def __init__(self, params):
        super().__init__(params)
        self._url = params['url']
        self._soup = params['soup']
        self.orig_post_id = self._extract_orig_post_id()
        self.orig_url = f'https://www.instagram.com/p/{self.orig_post_id}/'

    @property
    def identifier(self):
        return self.orig_post_id

    def _extract_orig_post_id(self):
        raw = str(self._soup)
        idx1 = raw.find('let short_code = ')
        cut1 = raw[idx1:]
        idx2 = cut1.find('"')
        cut2 = cut1[idx2+1:]
        idx3 = cut2.find('"')
        post_id = cut2[:idx3]
        return post_id

    @property
    def text(self):
        if self._text is None:
            if descrs := self._soup.select('div.single-photo-description'):
                self._text = (descrs[0].text or '').strip()
        return self._text or ''

    @property
    def author(self):
        if self._author is None:
            if nicks := self._soup.select('div.single-photo-nickname'):
                self._author = (nicks[0].text or '').strip()
        return self._author or ''

    @property
    def media(self):
        """
        Gather post images and videos in one list
        """
        if self._media is None:
            self._media = []
            self._media.extend([Image(url=url) for url in self._get_image_urls()])
            self._media.extend([Video(url=url) for url in self._get_video_urls()])
        return self._media

    def _find_img(self, soup):
        return find_elem(soup, 'img')

    def _find_vid(self, soup):
        return find_elem(soup, 'video')

    def _get_image_urls(self):
        img_urls = []

        if carousel := find_elem(self._soup, 'div.owl-carousel'):
            for item in carousel.select('div.item'):
                if img := self._find_img(item):
                    img_urls.append(img.attrs['src'])
        else:
            if single := find_elem(self._soup, 'div.single-photo'):
                if not self._find_vid(single):
                    img = self._find_img(single)
                    img_urls.append(img.attrs['src'])

        return img_urls

    def _get_video_urls(self):
        vid_urls = []

        if carousel := find_elem(self._soup, 'div.owl-carousel'):
            for item in carousel.select('div.item'):
                if vid := self._find_vid(item):
                    if url := vid.attrs.get('src'):
                        vid_urls.append(url)
        else:
            if single := find_elem(self._soup, 'div.single-photo'):
                if vid := self._find_vid(single):
                    if url := vid.attrs.get('src'):
                        vid_urls.append(url)

        return vid_urls


class GramhirSource(InstagramSource):
    """
    Instagram client that uses gramhir.com
    """
    def __init__(self, name, params):
        super().__init__(name, params)
        self._gramhir_id = params['id']

        self.nickname = self._gramhir_id.split('/')[0]
        self.url = self._construct_url(params)
        self.orig_url = f'https://www.instagram.com/{self.nickname}/'
        self.init_session()

    def _construct_url(self, params):
        if 'gramhir' not in CONFIG.gramhir_host:
            profile_id = params['id'].split('/')[0]

        url = f'https://{CONFIG.gramhir_host}/profile/{profile_id}'
        return url

    def open_profile(self):
        try:
            self.open(self.url)
            for i in range(3):
                self._client.scroll_up_down()
        except Exception as exc:
            logger.error('Cant open profile: %s', exc)

    def get_last_posts(self):
        """
        Get list of Post instances of posts
        which appeared after the last check
        """
        posts = []
        urls = self._parse_post_urls()
        if not urls:
            logger.info('Something went wrong, no last posts found on the page')

        for url in urls:
            try:
                self.open(url)
            except Exception as exc:
                logger.info('Skipping post %s because of error: %s', url, exc)
            else:
                posts.append(GramhirPost({'url': url, 'soup': self.get_soup()}))
            time.sleep(CONFIG.delay_after_post)

        return posts

    def get_last_stories(self):
        stories = []
        # TODO
        return stories

    def get_updates(self):
        """
        Get list of Update instances of update
        which appeared after the last check
        """
        updates = []
        self.open_profile()

        updates += self.get_last_posts()
        updates += self.get_last_stories()
        return updates

    def _parse_post_urls(self):
        """
        Get post URLs from the provided profile soup
        """
        soup = self.get_soup()

        urls = []
        for div in soup.select('div.photo'):
            if as_ := div.select('a'):
                if href := as_[0].attrs.get('href'):
                    urls.append(href)

        if ip_in_string(CONFIG.gramhir_host):
            urls = [u.replace(CONFIG.gramhir_host_header, CONFIG.gramhir_host) for u in urls]

        return urls[::-1]


class GramhirSeleniumSource(GramhirSource, SeleniumSource):
    pass


class GramhirRequestsSource(GramhirSource, RequestsSource):

    def http_get(self, url, headers=None):
        headers = headers or {}
        if ip_in_string(url) and not headers.get('Host'):
            headers['Host'] = CONFIG.gramhir_host_header

        resp = super().http_get(url, headers=headers)
        return resp


class InstaloaderSource(InstagramSource):
    """
    Instagram client that uses instaloader lib
    """
    def __init__(self, name, params):
        super().__init__(name, params)
        self.nickname = params['id']
        self._il = instaloader.Instaloader()

    def open_profile(self):
        return instaloader.Profile.from_username(self._il.context, self.nickname)

    def get_last_posts(self):
        """
        Get list of Post instances of posts
        which appeared after the last check
        """
        posts = []
        for idx, ilpost in enumerate(self._profile.get_posts()):
            posts.append(InstaloaderPost(ilpost))
            if idx > 10:
                break
            time.sleep(CONFIG.delay_after_post)

        return posts

    def get_last_stories(self):
        stories = []
        # TODO
        return stories

    def get_updates(self):
        """
        Get list of Update instances of update
        which appeared after the last check
        """
        updates = []
        self._profile = self.open_profile()

        updates += self.get_last_posts()
        updates += self.get_last_stories()
        return updates


class InstaloaderPost(InstagramPost):
    """
    Post handler for Instaloader source
    """
    def __init__(self, ilpost):
        self._author = f'@{ilpost.owner_username}'
        self._date = ilpost.date_utc
        self._text = ilpost.caption
        self._url = f'https://www.instagram.com/p/{ilpost.shortcode}'
        self._ilpost = ilpost

        self.orig_post_id = ilpost.shortcode

    @property
    def identifier(self):
        return self.orig_post_id

    @property
    def media(self):
        """
        Gather post images and videos in one list
        """
        if self._media is None:
            self._media = []

            for node in self._ilpost.get_sidecar_nodes():
                if node.is_video:
                    self._media.append(Video(url=node.video_url))
                else:
                    self._media.append(Image(url=node.display_url))

            if not self._media:
                if self._ilpost.is_video:
                    self._media.append(Video(url=self._ilpost.video_url))
                else:
                    self._media.append(Image(url=self._ilpost.url))

        return self._media
