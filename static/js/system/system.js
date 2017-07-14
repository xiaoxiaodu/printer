/*
Copyright (c) 2011-2012 Weizoom Inc
*/
W = {
	dev: {},
	registry: {},
	common: {model:{}},
	util: {},
	uirole: {},
	ueditor: {},
	mall: {},
	member: {},
	weixin2: {},
	//for termite
	data: {mobile:{}, viper:{}},
	design: {},
	util: {
		$M:null, //$M是iframe中的jQuery
		mobilePageDragComponentHandler: $.noop,
		changeComponentInDesignPageHandlers: [], //design page中切换component的响应函数集合
		getInsertIndicatorLayoutInMobilePage: $.noop
	},
	view: {
		cssEditorView: null,
	}
}

/**
 * W.registerUIRole: 每一个widget(view)，通过该函数向W中注册一个ui role，由W负责统一初始化
 *   selector: ui role的selector
 *   initializer: 初始化函数
 */
W.registerUIRole = function(selector, initializer) {
	W.uirole[selector] = initializer;	
}

W.createWidgets = function($node) {
	if (!$node) {
		$node = $;
	}
	_.each(W.uirole, function(initializer, selector) {
		var $uiViews = $node.find(selector);
		if ($uiViews.length > 0) {
			xlog("[W] init ui role: '" + selector + "'");
			xlog($uiViews);
			$uiViews.each(function() {
				var $uiView = $(this);
				if ($uiView.data('view')) {
					return;
				} else {
					initializer.call(this);
				}
			});
		}
	});
}

$(document).ready(function(event) {
	_.each(W.uirole, function(initializer, selector) {
		var $uiViews = $(selector);
		if ($uiViews.length > 0) {
			xlog("[W] init ui role: '" + selector + "'");
			$uiViews.each(initializer);
		}
	});
});

W.reload = function() {
	window.location.reload();
}

W.loadJSON = function(id) {
	var text = $.trim($('#__json-'+id).text());
	if (text) {
		return $.parseJSON(text);
	} else {
		return null;
	}
}

W.toFormData = function(data) {
	var newData = {};
	_.map(data, function(value, key){
		if ($.isArray(value) || $.isPlainObject(value)) {
			newData[key] = JSON.stringify(value);
		} else {
			newData[key] = value;
		}
	});

	return newData;
}

function ensureNS(ns) {
	var items = ns.split('.');
	var obj = window;
	for (var i = 0; i < items.length; ++i) {
		var item = items[i];
        if (!obj.hasOwnProperty(item)) {
            obj[item] = {}
        }
        obj = obj[item];
	}
}

function xlog(msg) {
	if (window.console) {
		window.console.info(msg);
	}
}

function xwarn(msg) {
	if (window.console) {
		window.console.warn(msg);
	}
}

function xerror(msg) {
	if (window.console) {
		window.console.error(msg);
	}
}

/**
 * parseUrl: 简单解析url，解析结果为:
 *  baseUrl: ?部分之前的url
 *  query: query string的array
 */
function parseUrl(url) {
	var result = {baseUrl:'', query:{}}
	var pos = url.indexOf('?');
	if (pos === -1) {
		result.baseUrl = url;
		return result;
	}

	result.baseUrl = url.substring(0, pos);

	var queryString = url.substring(pos+1);
	var querys = queryString.split('&');
	var count = querys.length;
	for (var i = 0; i < count; ++i) {
		var query = querys[i];
		var items = query.split('=');
		result.query[items[0]] = items[1];
	}

	return result;
}

W.animate = function($node, klass, callback) {
	klass = 'xui-designView-animated ' + klass;
	$node.addClass(klass);
	if (!callback) {
		callback = $.noop;
	}
	$node.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
		$node.removeClass(klass);
		callback();
	});
}


/*按扭LOADING*/
$.fn.bottonLoading = function (options) {
	var el = this;
	if(!el.find('span.img').length) {
		el.prepend('<span class="img"></span>');
	}
	switch(options.status) {
	case 'show':
		el.addClass('submitting');
		el.attr('disabled', true);
		break;
	case 'hide':
		el.removeClass('submitting');
		el.attr('disabled', false);
		break;
	}
}

$.fn.serializeObject = function(options) {
	var $form = $(this);
	var datas = $form.serializeArray();
	var obj = {};
	for (var i = 0; i < datas.length; ++i) {
		var data = datas[i];
		obj[data.name] = data.value;
	}

	return obj;
}




/**
 * 扩展underscore _.clone
 */
_.deepClone = function(obj) {
	if (!_.isObject(obj)) return obj;
	if (_.isFunction(obj)) return obj;
	var isArr = (_.isArray(obj) || _.isArguments(obj));
	var func = function (memo, value, key) {
		if (isArr) {
			memo.push(_.deepClone(value));
		} else {
			memo[key] = _.deepClone(value);
		}
		return memo;
	};
	return _.reduce(obj, func, isArr ? [] : {});
}


Handlebars.registerHelper('ifCond', function (v1, operator, v2, options) {
    switch (operator) {
        case '==':
            return (v1 == v2) ? options.fn(this) : options.inverse(this);
        case '===':
            return (v1 === v2) ? options.fn(this) : options.inverse(this);
        case '<':
            return (v1 < v2) ? options.fn(this) : options.inverse(this);
        case '<=':
            return (v1 <= v2) ? options.fn(this) : options.inverse(this);
        case '>':
            return (v1 > v2) ? options.fn(this) : options.inverse(this);
        case '>=':
            return (v1 >= v2) ? options.fn(this) : options.inverse(this);
        case '&&':
            return (v1 && v2) ? options.fn(this) : options.inverse(this);
        case '||':
            return (v1 || v2) ? options.fn(this) : options.inverse(this);
        default:
            return options.inverse(this);
    }
});


Handlebars.registerHelper('checkWhetherSelectOption', function (component, field, option, options) {
	if (component.model.get(field.name) === option.value) {
    	return 'selected'
    } else {
    	return ''
    }
});

Handlebars.registerHelper('getComponentPropertyValue', function (component, field, options) {
	var value = component.model.get(field.name);
	if (value) {
		return value;
	} else {
		return '';
	}
});

Handlebars.registerHelper('formatPositionAndSize', function (component, options) {
	return "width:" + component.model.width + 'px; height:' + component.model.height + 'px;';
});


// 系统错误码
W.SUCCESS = 200;