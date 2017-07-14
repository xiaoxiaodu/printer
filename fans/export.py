# -*- coding: utf-8 -*-

FIRST_NAV = 'fans'


SECOND_NAVS = [{
	'name': 'outline',
	'text': '粉丝概况',
	'url': '/fans/outline/'
}, {
	'name': 'fans',
	'text': '粉丝列表',
	'url': '/fans/fanses/'
}, {
	'name': 'card',
	'text': '微众卡发放',
	'url': '/fans/cards/'
}, {
	'name': 'total_suggestions',
	'text': '反馈意见',
	'url': '/fans/total_suggestions/'
}, {
	'name': 'coupon_history',
	'text': '优惠券发放记录',
	'url': '/fans/coupon_history/'
},{
	'name': 'qrcode_effect',
	'text': '渠道扫码效果',
	'url': '/fans/qrcode_effect/'
},{
	'name': 'consumption_statistics',
	'text': '消费金额统计',
	'url': '/fans/consumption_statistics/'
},{
	'name': 'supplier_products',
	'text': '八千供货商统计',
	'url': '/fans/supplier_products/'
}



]


def get_second_navs(request):
	return SECOND_NAVS