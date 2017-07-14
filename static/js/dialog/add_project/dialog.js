/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 添加项目对话框
 * 
 */
ensureNS('W.macaron.dialog');
W.macaron.dialog.AddProjectDialog = W.dialog.Dialog.extend({
    
    templates: {
        dialogTmpl: '#system-add-project-dialog-tmpl-src'
    },

    onInitialize: function(options) {
    },

    beforeShow: function(options) {
        this.$dialog.find('[name="name"]').val('');
        this.$dialog.find('[name="description"]').val('');
    },

    onShow: function(options) {
        var _this = this;
        _.delay(function() {
            if (options.projectId) {
                W.getApi().call({
                    app: 'project',
                    api: 'project/get',
                    args: {
                        project_id: options.projectId
                    },
                    success: function(data) {
                        _this.$dialog.find('[name="description"]').val(data.description);
                        _this.$dialog.find('#project-name-input').val(data.name).focus();
                    },
                    error: function(resp) {
                        alert('ha');
                    }
                })
            } else {
                _this.$dialog.find('#project-name-input').focus();
            }
            
        }, 300);
    },

    afterShow: function(options) {
    },

    /**
     * onClickSubmitButton: 点击“完成”按钮后的响应函数
     */
    onGetData: function(event) {
        if (!W.validate(this.$dialog)) {
            return null;
        }

        var name = this.$dialog.find('[name="name"]').val();
        var description = this.$dialog.find('[name="description"]').val();

        return {
            name: name,
            description: description
        };
    }
});