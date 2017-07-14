#coding: utf8

import hashlib, re, string

HTML_TAG_PATTERN = re.compile('<[^>]+>')

def filter_html_tag(content):
	if isinstance(content, unicode):
		content = content.encode('utf-8')
	
	content = HTML_TAG_PATTERN.sub("", content)
	return content


def clean_content(content):
	#过滤html标签
	content = filter_html_tag(content)

	#过滤调研问题名称
	# lines = content.split('\n')
	# new_content = ''
	# for line in lines:
	# 	line = line.strip()
	# 	if line != '':
	# 		_lines = re.split(':|：', line)
	# 		if len(_lines) > 1:
	# 			_lines = _lines[1:]
	# 		new_content += ':'.join(_lines) + '\n'

	# content = new_content

	#过滤标点符号、空白符、换行符
	#TODO 中文标点也需要过滤
	content = content.translate(None, string.punctuation).translate(None, string.whitespace)
	return content


def clean_content_for_similarity(content):
	#过滤html标签
	content = filter_html_tag(content)

	#过滤调研问题名称
	lines = content.split('\n')
	new_content = ''
	for line in lines:
		line = line.strip()
		if line != '':
			_lines = re.split(':|：', line)
			if len(_lines) > 1:
				_lines = _lines[1:]
			new_content += ':'.join(_lines) + '\n'

	content = new_content

	#过滤标点符号、空白符、换行符
	#TODO 中文标点也需要过滤
	content = content.translate(None, string.punctuation).translate(None, string.whitespace)
	return content


VALID_CONTENT_LEN = 10
def is_useless_content(content):
	"""
	判断一个调研内容是不是无用的回答，如果长度小于10则认为一条回答没有意义
	"""
	#过滤html标签
	content = filter_html_tag(content)

	#过滤调研问题名称
	lines = content.split('\n')
	for line in lines:
		line = line.strip()
		if line != '':
			_lines = re.split(':|：', line)
			if len(_lines) > 1:
				line = "".join(_lines[1:])
			
			if len(line.decode('utf-8')) > VALID_CONTENT_LEN:
				return False

	return True


def text2md5(text):
	"""
	文本转MD5(32字节hex string)
	"""
	text = clean_content(text)
	return clean_text2md5(text)


def clean_text2md5(text):
	"""
	文本转MD5(32字节hex string)
	"""
	m = hashlib.md5()
	if isinstance(text, unicode):
		m.update(text.encode('utf8'))
	else:
		m.update(text)
	return m.hexdigest()