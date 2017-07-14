/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 添加项目对话框
 * 
 */
ensureNS('W.macaron.dialog');
W.macaron.dialog.EditUserDialog = W.dialog.Dialog.extend({

    templates: {
        dialogTmpl: '#system-edit-user-dialog-tmpl-src'
    },

    onInitialize: function(options) {
        /*
        var selector = 'input[data-ui-role="image-selector"]';
        W.uirole[selector].call(this.$dialog.find(selector));
        this.imageView = this.$dialog.find('input[data-ui-role="image-selector"]').data('view');
        */
    },

    beforeShow: function(options) {
        this.$dialog.find('[name="name"]').val('');
        this.$dialog.find('[name="real_name"]').val('');
        this.$dialog.find('[name="password"]').val('');
        this.$dialog.find('[name="email"]').val('');
        //this.$dialog.find('[name="thumbnail"]').val('');
        //this.$dialog.find('[name="wip"]').val('');

        //this.imageView.cleanImage();
        this.$dialog.find('.errorHint').hide();

        if (options.userId) {
            this.$dialog.find('.modal-title').text('编辑用户');
            this.$dialog.find('[name="password"]').removeAttr('data-validate');
            this.$dialog.find('[name="password"]').parents('.form-group').find('label').removeClass('xui-validate-star');
        } else {
            this.$dialog.find('.modal-title').text('添加用户');
            this.$dialog.find('[name="password"]').attr('data-validate', 'required');
            this.$dialog.find('[name="password"]').parents('.form-group').find('label').addClass('xui-validate-star');
        }
    },

    onShow: function(options) {
        var _this = this;
        
        _.delay(function() {
            if (options.userId) {
                W.getLoadingView().show();
                W.getApi().call({
                    app: 'user',
                    api: 'user/get',
                    args: {
                        user_id: options.userId
                    },
                    success: function(data) {
                        W.getLoadingView().hide();
                        _this.$dialog.find('[name="password"]').val('');
                        _this.$dialog.find('[name="name"]').val(data.name).focus();
                        _this.$dialog.find('[name="real_name"]').val(data.real_name);
                        _this.$dialog.find('[name="email"]').val(data.email);
                        //_this.$dialog.find('[name="thumbnail"]').val(data.thumbnail);
                        //_this.imageView.showImage(data.thumbnail);
                        //_this.$dialog.find('[name="wip"]').val(data.wip_count);
                    },
                    error: function(resp) {
                        W.getLoadingView().hide();
                    }
                })
            } else {
                _this.$dialog.find('[name="name"]').focus();
            }
            
        }, 500);
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
        var realName = this.$dialog.find('[name="real_name"]').val();
        var password = this.$dialog.find('[name="password"]').val();
        var email = this.$dialog.find('[name="email"]').val();
        //var thumbnail = this.$dialog.find('[name="thumbnail"]').val();
        //var wip = this.$dialog.find('[name="wip"]').val();

        return {
            name: name,
            password: password,
            email: email,
            real_name: realName
        };
    }
});