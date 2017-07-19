# -*- coding: utf-8 -*-

FIRST_NAV = 'mall'


SECOND_NAVS = [{
	'name': 'members',
	'text': '会员列表',
	'url': '/mall/members/'
}, {
	'name': 'malls',
	'text': '商户列表',
	'url': '/mall/malls/'
}
]


def get_second_navs(request):
	return SECOND_NAVS