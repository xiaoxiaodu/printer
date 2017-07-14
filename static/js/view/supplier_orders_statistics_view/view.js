/*
Copyright (c) 2011-2012 Weizoom Inc
*/
ensureNS('W.view.common');

W.view.common.StatisticsECharts = Backbone.View.extend({
    getTemplate: function() {
        $('#statistics-echart-tmpl-src').template('statistics-echart-tmpl');
        return 'statistics-echart-tmpl';
    },

    events: {
        'click .xa-switchingBtn': 'onClickShortcut'
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.$el.removeData('view');
        this.options = options;
        this.options['api'] = this.$el.attr('data-api');
        this.options['app'] = this.$el.attr('data-app');
        this.options['resource'] = this.$el.attr('data-resource');
        this.options['type'] = this.$el.attr('data-type') || "chart";
        this.options['wrapEl'] = this.$el.attr('data-wrap-el') || null;
        this.options['ponint'] = this.$el.attr('data-ponint') || 7;
        var isActive = this.$el.attr('data-isactive');
        var args = this.$el.attr('data-args');
        if (args) {
            this.args = $.parseJSON(args);
        }
        this.title = options.title;
        this.type = this.options['type'];
        this.wrapEl = this.options['wrapEl'];
        this.ponint = this.options['ponint'];
        this.sign = this.options.sign || 'W';
        this.isExternal = this.$el.attr('data-is-external') || 'false';
        this.chartPrompt = options.chartPrompt;
        this.template = this.getTemplate();

        this.$el.data('view', this);
    },

    render: function() {
        this.$el.addClass("wui-echart");
        var data = {
            id: this.$el.attr('id'),
            title: this.title
        }
        var $node = $.tmpl(this.template, data);

        this.$el.append($node);
        // W.createWidgets(this.$el);
        this.$chart = this.$('.wui-i-content').eq(0);

        // var onSelectDate = _.bind(this.onSelectDate, this);
        // this.startDateView = this.$('[name="start_date"]').data('view');
        // this.startDateView.on('select-date', onSelectDate);
        // this.endDateView = this.$('[name="end_date"]').data('view');
        // this.endDateView.on('select-date', onSelectDate);
        this.load();
    },

    reload: function(options) {
        this.load();
    },

    load: function(options) {

        this.loadChart(this.args)
    },

    loadChart: function(args) {
        var _this = this;
        var host = W.wglass_host;
            W.getApi().call({
                app: this.options.app,
                api: this.options.resource,
                method: 'get',
                args: args,
                scope: this,
                success: function(data) {
                    var option = data;
                    var myChart = echarts.init(_this.$chart.get(0));
                    // 为echarts对象加载数据 
                    console.log(option);
                    $("#static_date_internal").html(option['xAxis']['data'][0]+"至"+option['xAxis']['data'][option['xAxis']['data'].length -1])

                    myChart.setOption(option);
                    $('.xui-loading').css('display', 'none');
                },
                error: function(resp) {
                    // alert('获取统计数据失败!');
                    $('.xui-loading').css('display', 'none');
                }
            });

    },

    pic_data_render: function(char_data) {
        var type = char_data.type || 'table';
        if (data.type == 'table') {
            return;
        }
        var show_pic_data = data.data;
        var $div = this.$el.parent('div').find('.xa-interlockChart');
        var myChart = echarts.init($div[0]);
        // 为echarts对象加载数据 
        myChart.setOption(data);
    },

    //TODO 完成独立的表格组件
    loadTable: function(args) {
        var advancedTable = new W.view.common.AdvancedTable({
            el: this.$el,
            template: '#table-view-box-tmpl-src',
            app: this.options.app,
            api: this.options.api,
            args: JSON.stringify(args),
            enablePaginator: true,
            enableSort: false,
            pic: this.show_pic
        });
        advancedTable.render();

        $(this).data('view', advancedTable);
    },

    onClickShortcut: function(event) {
        $('.xui-loading').css('display', 'block');
        var value = $(event.currentTarget).attr('data-value');
        this.$('.xui-active').removeClass('xui-active');
        $(event.target).addClass('xui-active');
        this.sign = value;
        this.load();
    },

    onSelectDate: function(date) {
        this.$('.wui-i-activeLink').removeClass('wui-i-activeLink');
        this.load()
    },

    get_chart_option: function(dates, values){
        var options = {
            // 'fdg': 234
            'xAxis': {
                'axisLine': {
                    'onZero': false
                },
                'axisLabel': {
                    'formatter': "{value}"
                },
                'data': dates
            },
            'yAxis': {
                'axisLabel': {
                    'formatter': "{value}"
                },
                'type': "value"
            },
            'calculable': true,
            'toolbox': {
                'show': false
            },
            'tooltip': {
                'trigger': "axis"
            },
            'legend': {
                'x': "left",
                'data': [
                    this.chartPrompt
                ],
                'orient': "horizontal",
                'show': false
            },
            'series': [{
                'smooth': true,
                'type': "line",
                'name': this.chartPrompt,
                'data': values
            }]
        };  
        console.log(options)
        return options
    }
});
