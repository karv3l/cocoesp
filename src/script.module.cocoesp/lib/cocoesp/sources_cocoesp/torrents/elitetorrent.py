# -*- coding: utf-8 -*-
"""
	cocoesp - Elite Torrent (castellano). Spec 006.
	Búsqueda y rutas basadas en el canal de Alfa (alfa-addon/addon, GPL-3.0).
"""
from cocoesp.modules.spanish_sites import SpanishTorrentSite


class source(SpanishTorrentSite):
	site_name = 'elitetorrent'
	url_setting = 'elitetorrent.url'
	default_domain = 'https://www.elitetorrent.com'
	search_path = '/?s=%s&x=0&y=0'
	movie_link_re = r'/peliculas/[^/?#]+'
