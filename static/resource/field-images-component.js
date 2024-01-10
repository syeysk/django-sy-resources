FieldImagesComponent = {
    props: ['name', 'modelValue'],
    emits: ['update:modelValue'],
    //data () {
    //    return {files: []};
    //},
    /*
    computed: {
        value: {
            get() {
               return this.modelValue;
            },
            set(value) {
               this.$emit('update:modelValue', value);
            },
        },
    },
    */
    methods: {
        set_value(event) {
            //let file_field = event.target;
            //this.files = file_field.files;
            //this.$emit('update:modelValue', []);
        },
        //get_files() {
        //    return this.files;
        //},
    },
    template: `
        <div style="text-align: center;">
            <div v-for="image in modelValue" style="display: inline-block; margin-right: 15px; position: relative;">
                <img style="width: 100px;" :src="image.image" :key="image.pk">
                <span class="del_btn" style="position: absolute; top: -5px; right: -5px; border-radius: 7px; width: 20px; height: 20px; border: solid red 2px; cursor: pointer; color: red;" title="удалить фотографию">x</span>
                <input name="is_main" :checked="image.is_main" style="position: absolute; top: -5px; right: 20px; cursor: pointer;" title="сделать главным фото" type="radio">
            </div>
        </div>
        <div class="mb-3 form-group" :id="name + '-group'">
            <div class="form-floating">
                <input @change="set_value" class="form-control" type="file" :name="name" :id="name + '-field'" v-bind="$attrs" multiple>
                <label :for="name + '-field'" class="form-label"><slot/></label>
            </div>
        </div>
    `,
}
