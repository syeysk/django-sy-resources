ResourceComponent = {
    props: [],
    components: {FieldEditorComponent},
    data() {
        $('h1')[0].textContent = '';
        let resource_object = JSON.parse(document.getElementById('resource_json').textContent);
        let isNew = !Boolean(resource_object);
        return {
            title: isNew ? '' : resource_object.title,
            status: isNew ? '' : resource_object.status,
            //description: isNew ? '' : project_object.description,
            //seo_description: isNew ? '' : project_object.seo_description,
            //seo_keywords: isNew ? '' : project_object.seo_keywords,
            isNew: isNew,
            has_access_to_edit: HAS_ACCESS_TO_EDIT,
        };
    },
    methods: {
        save_resource(event, fieldComponent) {
            let self = this;
            let form = event.target.form;
            data = {};
            data[fieldComponent.name] = fieldComponent.value;
            if (this.isNew) {
                $.ajax({
                    url: window.location.href + URL_RESOURCE,
                    headers: {'X-CSRFToken': CSRF_TOKEN},
                    dataType: 'json',
                    contentType: 'application/json',
                    processData: false,
                    data: JSON.stringify(data),
                    success: function(result) {
                        fieldComponent.errorMessage = '';
                        history.pushState(
                            null,
                            null,
                            location.href.replace('/new', '/' + result.project_id),
                        );
                        fieldComponent.set_view();
                        self.isNew = false;
                    },
                    statusCode: {
                        500: function(xhr) {
                            clear_status_fields(form);
                            self.errorMessage = 'ошибка создания';
                        },
                        400: function(xhr) {
                            self.errorMessage = '';
                            clear_status_fields(form);
                            set_invalid_field(form, xhr.responseJSON);
                        },
                    },
                    method:'post',
                });
            } else {
                $.ajax({
                    url: window.location.href + URL_RESOURCE,
                    headers: {'X-CSRFToken': CSRF_TOKEN},
                    dataType: 'json',
                    contentType: 'application/json',
                    processData: false,
                    data: JSON.stringify(data),
                    success: function(result) {
                        clear_status_fields(form);
                        set_valid_field(form, result.updated_fields);
                        self.successMessage = '';
                        fieldComponent.set_view();
                    },
                    statusCode: {
                        500: function(xhr) {
                            clear_status_fields(form);
                            self.errorMessage = 'ошибка сохранения';
                        },
                        400: function(xhr) {
                            self.errorMessage = '';
                            clear_status_fields(form);
                            set_invalid_field(form, xhr.responseJSON);
                        },
                    },
                    method:'post',
                });
            }
        },
    },
    template: `
        <field-editor-component
						 name-editor-component="field-input-component"
						 name-viewer-component="teleport-to-header-component"
						 v-model="title"
						 name="title"
						 :is-edit="isNew"
						 @save="save_resource"
						 verbose-name="Наименование ресурса"
						 :show-cancel-btn="!isNew"
				>[[ title ]]</field-editor-component>
    `,
}
