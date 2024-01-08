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
        <div class="mb-3 form-group" :id="name + '-group'">
            <div class="form-floating">
                <input @change="set_value" class="form-control" type="file" :name="name" :id="name + '-field'" v-bind="$attrs" multiple>
                <label :for="name + '-field'" class="form-label"><slot/></label>
            </div>
        </div>
    `,
}
