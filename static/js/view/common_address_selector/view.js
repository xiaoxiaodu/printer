/*
Copyright (c) 2011-2012 Weizoom Inc
*/


ensureNS('W.view.common');
W.view.common.AddressSelector = Backbone.View.extend({	
	templates: {
		viewTmpl: '#common-address-selector-tmpl',
		cityTmpl: '#common-address-selector-tmpl-cities'
	},

	events: {
		'change .xa-province': 'onChangeProvince',
		'change .xa-city': 'onChangeCity'
	},
	
	isDisplayInfo: true,

	initialize: function(options) {
		this.$el = $(this.el);
		this.$input = this.$el;
		this.initAddress = $.trim(this.$input.attr('data-json'));
		if (this.initAddress.indexOf('{') !== -1) {
			this.initAddress = $.parseJSON(this.initAddress);
			var province = W.id2province[this.initAddress.province.id];
			if (province) {
				province.selected = true;
				var city = province.id2city[this.initAddress.city.id];
				if (city) {
					city.selected = true;
				}
			}
		} else {
			this.initAddress = null;
		}

		var $node = $('<div class="xa-addressSelector"></div>');
		this.$el.wrap($node);
		this.$el = this.$el.parent();
		this.el = this.$el.get(0);
	},

	render: function() {
		var context = {
			provinces: _.values(W.id2province)
		}
		var $node = this.renderTmpl('viewTmpl', context);
		this.$el.append($node);

		if (this.initAddress) {
			var event = {};
			event.currentTarget = this.$el.find('.xa-province').get(0);
			this.onChangeProvince(event);
		} else {
			this.updateAddressValue();	
		}
	},

	updateCities: function(id2city) {
		var context = {
			cities: _.values(id2city)
		}
		var $node = this.renderTmpl('cityTmpl', context);
		this.$el.find('.xa-city').empty().append($node);	
	},

	updateAddressValue: function() {
		var $province = this.$el.find('.xa-province');
		var provinceId = parseInt($province.val());
		var provinceName = '';
		if (provinceId !== 0) {
			provinceName = $province.find('option:checked').text();
		}

		var $city = this.$el.find('.xa-city');
		var cityId = parseInt($city.val());
		var cityName = '';
		if (cityId !== 0) {
			cityName = $city.find('option:checked').text();
		}

		var data = {
			province: {
				id: provinceId,
				name: provinceName
			},
			city: {
				id: cityId,
				name: cityName
			}
		}
		this.$input.val(JSON.stringify(data));
	},

	onChangeProvince: function(event) {
		var $select = $(event.currentTarget);
		var provinceId = parseInt($select.val());
		if (provinceId !== 0) {
			var id2city = W.id2province[$select.val()].id2city;
			this.updateCities(id2city);
		}
		this.updateAddressValue();
	},

	onChangeCity: function(event) {
		this.updateAddressValue();
	}
});

W.registerUIRole('[data-ui-role="address-selector"]', function() {
    var $el = $(this);
    var view = new W.view.common.AddressSelector({
        el: $el.get(0)
    });
    view.render();

    //缓存view
    $el.data('view', view);
});