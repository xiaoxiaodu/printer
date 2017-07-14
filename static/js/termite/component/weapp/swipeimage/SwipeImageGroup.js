/**
 * @class W.component.weapp.SwipeImageGroup
 * 
 */

ensureNS('W.component.weapp');
W.component.weapp.SwipeImageGroup = W.component.Component.extend({
	type: 'weapp.swipeimagegroup',
	shouldIgnoreSubComponent: true,
	dynamicComponentTypes: [
        {type: 'weapp.image', model: {index: 1, url: ''}}
    ],

	properties: [{
        group: '已选图片',
        fields: [{
            name: 'items',
            type: 'dynamic-generated-control',
            isUserProperty: true,
            default: []
        }]
    }],

	propertyChangeHandlers: {
		items: function($node, model, value) {
			var html = this.render();
			var $newNode = $(html);
			$node.empty().append($newNode.children());

			W.Broadcaster.trigger('component:click', this);
        },
	},

	render: function() {
		var buf = [];
		buf.push('<div class="xa-component xui-swipeImageGroup" data-cid="'+this.cid+'">');
		if (this.components.length === 0) {
			buf.push('轮播图');
		} else {
			for (var i = 0; i < this.components.length; ++i) {
				var subComponent = this.components[i];
				buf.push(subComponent.render());
			}
		}
		buf.push('</div>');
		return buf.join('');
	}
}, {
	indicator: {
		name: '轮播图',
		imgClass: 'componentList_component_swipe_image'
	}
});
