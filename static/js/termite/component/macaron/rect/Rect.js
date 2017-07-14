/**
 * @class W.component.macaron.Rect
 * 页面
 */
ensureNS('W.component.macaron');
W.component.macaron.Rect = W.component.Component.extend({
	type: 'macaron.rect',
	category: 'shape',

	properties: [
        {
            group: '',
            groupClass: '',
            fields: [{
                name: 'fill_color',
				type: 'color_picker',
				displayName: '填充',
				isUserProperty: true,
				default: '#42C2B3'
            }, {
                name: 'width',
                type: 'text',
                displayName: '宽',
                isUserProperty: true,
                default: '100'
            }, {
                name: 'height',
                type: 'text',
                displayName: '高',
                isUserProperty: true,
                default: '100'
            }, {
                name: 'x',
                type: 'text',
                displayName: 'X',
                isUserProperty: true,
                default: '100'
            }, {
                name: 'y',
                type: 'text',
                displayName: 'Y',
                isUserProperty: true,
                default: '100'
            }]
        }
    ],

});
