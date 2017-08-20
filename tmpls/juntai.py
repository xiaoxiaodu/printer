# -*- coding: utf-8-*-

import random
import win32com
import pythoncom
from datetime import datetime
from win32com.client import Dispatch, constants
from datetime import datetime

from mall import models as mall_models

def print1(member_id, mall_id, card_id, products_info):
	member = mall_models.Member.objects.get(id=member_id)
	mall = mall_models.Mall.objects.get(id=mall_id)
	card = mall_models.MemberHasCard.objects.get(id=card_id)

	__print_xiaopiao(member, mall, card, products_info)

def __print_xiaopiao(member, mall, card, products_info):
	products = mall_models.Product.objects.filter(id__in=products_info.keys())
	total_price = 0
	total_num = 0
	product_str = u""
	sale_id = random.randint(3640000000, 3999990086)
	for product in products:
		num = int(products_info[str(product.id)])
		price = product.price * num
		total_num += num
		total_price += price

		name = product.name
		if len(name) < 12:
			name += ' ' * (12 - len(name))
		product_line = "%s %d    %.2f    %.2f" % (name, num, product.price, price)
		product_str += u"销售单号： %s\r\n%s\r\n" % (sale_id, product_line)
		sale_id += random.randint(10, 200)
	card_number = card.card_number[0:-11] + '******' + card.card_number[-4:]

	liushui = '00%d' % random.randint(30000, 99999)
	shouyin = '000%d' % random.randint(101, 109)
	jihao = '0%d' % random.randint(301, 310)
	date = datetime.now().strftime('%Y-%m-%H')
	time = datetime.now().strftime('%H:%M')
	#模板文件保存路径，此处使用的是绝对路径，相对路径未测试过
	template_path = u'D:\\tmpl\\北京君太百货小票.docx'
	#另存文件路径，需要提前建好文件夹，不然会出错
	store_path = u'D:\\tmpl\\temp\\'
	
	#启动word
	pythoncom.CoInitialize()
	w = win32com.client.Dispatch('Word.Application')
	# 或者使用下面的方法，使用启动独立的进程：
	# w = win32com.client.DispatchEx('Word.Application')
	
	# 后台运行，不显示，不警告
	w.Visible = 0
	w.DisplayAlerts = 0
	# 打开新的文件
	doc = w.Documents.Open(FileName=template_path)
	# worddoc = w.Documents.Add() # 创建新的文档
	
	# 正文文字替换
	w.Selection.Find.ClearFormatting()
	w.Selection.Find.Replacement.ClearFormatting()

	w.Selection.Find.Execute('{{liushui}}', False, False, False, False, False, True, 1, True, liushui, 2)
	w.Selection.Find.Execute('{{shouyin}}', False, False, False, False, False, True, 1, True, shouyin, 2)
	w.Selection.Find.Execute('{{jihao}}', False, False, False, False, False, True, 1, True, jihao, 2)
	w.Selection.Find.Execute('{{date}}', False, False, False, False, False, True, 1, True, date, 2)
	w.Selection.Find.Execute('{{time}}', False, False, False, False, False, True, 1, True, time, 2)

	w.Selection.Find.Execute('{{line}}', False, False, False, False, False, True, 1, True, product_str, 2)

	w.Selection.Find.Execute('{{num}}', False, False, False, False, False, True, 1, True, total_num, 2)
	w.Selection.Find.Execute('{{total_price}}', False, False, False, False, False, True, 1, True, '%.2f' % total_price, 2)
	w.Selection.Find.Execute('{{card_number}}', False, False, False, False, False, True, 1, True, card_number, 2)
	w.Selection.Find.Execute('{{time}}', False, False, False, False, False, True, 1, True, time, 2)

	w.Selection.Find.Execute('{{bank}}', False, False, False, False, False, True, 1, True, card.bank_name, 2)

	datestr = datetime.now().strftime('%Y%m%H%M%S')
	doc.SaveAs(store_path + u'北京君太百货小票-%s-%s.docx' % (member.name, datestr))
	doc.PrintOut()
	
	# w.Documents.Close()
	doc.Close()
	w.Quit()
	w = None

	__print_yinlian(card, member, total_price, datestr)

def __print_yinlian(card, member, total_price, datestr):
	card_number = card.card_number[0:-11] + '******' + card.card_number[-4:]
	valid_time = card.valid_time
	invoice_no = '00%d' % random.randint(301, 999)
	voucher_no = '%d' % random.randint(100001, 150000)
	trace_no = '%d' % random.randint(100001, 150000)
	date = datetime.now().strftime('%Y/%m/%H')
	time = datetime.now().strftime('%H:%M:%S')
	refeno = '%d' % random.randint(600000000009, 699999999999)

	#模板文件保存路径，此处使用的是绝对路径，相对路径未测试过
	template_path = u'D:\\tmpl\\北京君太百货银联.docx'
	#另存文件路径，需要提前建好文件夹，不然会出错
	store_path = u'D:\\tmpl\\temp\\'
	
	#启动word
	pythoncom.CoInitialize()
	w = win32com.client.Dispatch('Word.Application')
	# 或者使用下面的方法，使用启动独立的进程：
	# w = win32com.client.DispatchEx('Word.Application')
	
	# 后台运行，不显示，不警告
	w.Visible = 0
	w.DisplayAlerts = 0
	# 打开新的文件
	doc = w.Documents.Open(FileName=template_path)
	# worddoc = w.Documents.Add() # 创建新的文档
	
	# 正文文字替换
	w.Selection.Find.ClearFormatting()
	w.Selection.Find.Replacement.ClearFormatting()

	w.Selection.Find.Execute('{{card_number}}', False, False, False, False, False, True, 1, True, card_number, 2)
	w.Selection.Find.Execute('{{inv}}', False, False, False, False, False, True, 1, True, invoice_no, 2)
	w.Selection.Find.Execute('{{vou}}', False, False, False, False, False, True, 1, True, voucher_no, 2)
	w.Selection.Find.Execute('{{trace}}', False, False, False, False, False, True, 1, True, trace_no, 2)
	w.Selection.Find.Execute('{{date}}', False, False, False, False, False, True, 1, True, date, 2)
	w.Selection.Find.Execute('{{time}}', False, False, False, False, False, True, 1, True, time, 2)
	w.Selection.Find.Execute('{{refe}}', False, False, False, False, False, True, 1, True, refeno, 2)
	w.Selection.Find.Execute('{{valid}}', False, False, False, False, False, True, 1, True, valid_time, 2)
	w.Selection.Find.Execute('{{price}}', False, False, False, False, False, True, 1, True, '%.2f' % total_price, 2)


	doc.SaveAs(store_path + u'北京君太百货银联-%s-%s.docx' % (member.name, datestr))
	doc.PrintOut()
	
	doc.Close()
	# w.Documents.Close()
	w.Quit()
	w = None