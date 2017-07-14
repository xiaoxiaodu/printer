/**
 * @class W.component.weapp.Page
 * 页面
 */
ensureNS('W.component.macaron');
W.component.macaron.Page = W.component.Component.extend({
	type: 'macaron.page',
	category: 'page',

	properties: [
        {
            group: '',
            groupClass: '',
            fields: [{
                name: 'fill_color',
				type: 'color_picker',
				displayName: '填充',
				isUserProperty: true,
				default: '#FFF'
            }, {
                name: 'width',
                type: 'text',
                default: '370'
            }, {
                name: 'height',
                type: 'text',
                default: '600'
            }, {
                name: 'x',
                type: 'text',
                default: '10'
            }, {
                name: 'y',
                type: 'text',
                default: '10'
            }]
        }
    ],
});
