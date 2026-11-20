# -*- coding: utf-8 -*-
"""
	cocoesp - DonTorrent (castellano). Spec 006.
	Búsqueda y rutas basadas en el canal de Alfa (alfa-addon/addon, GPL-3.0).
	Muchas descargas de DonTorrent pasan por una prueba de trabajo antibot
	(api_validate_pow.php): NO se resuelve; solo se usan enlaces directos a .torrent/magnet.
"""
from cocoesp.modules.spanish_sites import SpanishTorrentSite


class source(SpanishTorrentSite):
	site_name = 'dontorrent'
	url_setting = 'dontorrent.url'
	default_domain = 'https://dontorrent.shopping'
	search_path = '/buscar'
	search_post = 'valor=%s&Buscar=Buscar&p=1'
	movie_link_re = r'/pelicula/[^/?#]+'
