# -*- coding: utf-8 -*-


FIRST_NAV = 'config'


SECOND_NAVS = [{
	'name': 'source',
	'text': '粉丝来源',
	'url': '/config/sources/'
}, 
# {
# 	'name': 'company',
# 	'text': '商家',
# 	'url': '/config/companies/'
# }, {
# 	'name': 'product',
# 	'text': '商品',
# 	'url': '/config/products/'
# }, {
# 	'name': 'suggestion_type',
# 	'text': '意见类型',
# 	'url': '/config/suggestion_types/'
# }, 
{
	'name': 'card',
	'text': '微众卡',
	'url': '/config/cards/'
}, {
	'name': 'weixin_account',
	'text': '服务微信号',
	'url': '/config/weixin_accounts/'
}]

WEIZOOM_SECOND_NAVS = [{
	'name': 'actor',
	'text': '操作人',
	'url': '/config/actors/'
}, {
	'name': 'coupon',
	'text': '优惠券',
	'url': '/config/coupons/'
},
{
	'name': 'qrcode',
	'text': '渠道扫码',
	'url': '/config/qrcodes/'
},
{
	'name': 'suggestion_ids_config',
	'text': '反馈id设置',
	'url': '/config/suggestion_ids/'
},
{
	'name': 'supplier_setting',
	'text': '供应商',
	'url': '/config/supplier_setting/'
},
{
	'name': 'supplier_products',
	'text': '八千商品管理',
	'url': '/config/supplier_products/'
}
]

MANAGER_SECOND_NAVS = [{
	'name': 'system_account',
	'text': '系统账号',
	'url': '/config/system_accounts/'
}, {
	'name': 'week_targets',
	'text': '周目标设定',
	'url': '/config/week_targets/'
}]


WEIZOOM_ACCOUNTS = ['jingxuan', 'mama', 'xuesheng', 'club']
def get_second_navs(request):
	if request.is_manager:
		navs = []
		navs.extend(SECOND_NAVS)
		navs.extend(WEIZOOM_SECOND_NAVS)
		navs.extend(MANAGER_SECOND_NAVS)
		return navs
	elif request.user.username in WEIZOOM_ACCOUNTS:
		navs = []
		navs.extend(SECOND_NAVS)
		navs.extend(WEIZOOM_SECOND_NAVS)
		return navs
	else:
		return SECOND_NAVS