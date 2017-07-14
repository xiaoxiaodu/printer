/**
 * @class W.component.weapp.Button
 * 
 */

ensureNS('W.component.weapp');
W.component.weapp.Button = W.component.Component.extend({
	type: 'weapp.button',

	properties: [{
		group: '属性组1',
		fields: [{
			name: 'text',
			isUserProperty: true,
			type: 'text',
			displayName: '标题',
			default: '修改标题...'
		}]
	}, {
		group: '属性组2',
		fields: [{
			name: 'color',
			isUserProperty: true,
			type: 'select',
			displayName: '颜色',
			source: [{name: "红色", value: "red"}, {name: "绿色", value: "green"}, {name: "蓝色", value: "blue"}],
			default: "green"
		}]
	}],

	propertyChangeHandlers: {
		text: function($node, model, value, $propertyViewNode) {
			$node.text(value);
		},

		color: function($node, model, value, $propertyViewNode) {
			if (value === 'green') {
				$node.removeClass('btn-primary btn-danger');
				$node.addClass('btn-success');
			} else if (value === 'blue') {
				$node.removeClass('btn-success btn-danger');
				$node.addClass('btn-primary');
			} else if (value === 'red') {
				$node.removeClass('btn-success btn-primary');
				$node.addClass('btn-danger');
			}
		}
	},

	render: function() {
		var html = '<a href="javascript:void(0);" class="btn btn-success xa-component" data-cid="'+this.cid+'" style="width: 150px; height: 150px;">'+this.model.get('text')+'</a>'
		return html;
	}
}, {
	indicator: {
		name: '按钮',
		imgClass: 'componentList_component_button'
	}
});
