<template>
    <div>
        <h1>{{ view_name }}</h1>
        <span
            v-for="input in input_data"
            :key="input.id">{{ input.display_text }}

            <SimpleNumberInput
                v-if="input.tag==='my_number'"
                v-model="input.value"
                :my_placeholder="input.placeholder"/>

            <SimpleDropdown v-else-if="input.tag==='my_dropdown'"
                v-model="input.value"
                :my_options="my_options[input.dropdown_key]"
                :my_placeholder="input.placeholder"/>

            <button @click="">{{ input.button_text }}</button>
        <br>
        </span>

        <form enctype="multipart/form-data" novalidate v-if="isInitial || isSaving">
            <h1>Upload Solar Data</h1>
            <div class="dropbox">
                <input type="file" multiple :name="uploadFieldName" :disabled="isSaving"
                       @change="filesChange($event.target.name, $event.target.files); fileCount = $event.target.files.length"
                       accept="image/*" class="input-file">

                    <p v-if="isInitial">Drag your file(s) here to begin<br>Or click to browse</p>
                    <p v-if="isSaving">Upload {{ fileCount }} files</p>
            </div>
        </form>
    </div>
</template>

<script>
    // Example code taken from https://scotch.io/tutorials/how-to-handle-file-uploads-in-vue-2

    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';

    import { upload } from "../../services/FileUpload";

    const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;

    export default {
        name: "Data",

        components: {
            SimpleDropdown,
            SimpleNumberInput,
        },

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "model_data",

                // File service attempts
                uploadedFiles: [],
                uploadError: null,
                currentStatus: null,
                uploadFieldName: 'photos',

                input_data: [
                    {
                        id: 0,
                        name: "solar_data_source",
                        display_text: "Solar Data Sources",
                        value: "",
                        dropdown_key: "solar_data_options",
                        placeholder: "Select One",
                        tag:"my_dropdown",
                        button_text:"Add",
                        add_function: this.add_solar_source(),
                    },
                    {
                        id: 1,
                        name: "load_data_source",
                        display_text: "Load Data Sources",
                        value: "",
                        dropdown_key: "load_data_options",
                        placeholder: "Select One",
                        tag:"my_dropdown",
                        button_text:"Add",
                        add_function: this.add_load_source(),
                    },
                ],

                my_options: {
                    solar_data_options: [
                        "Solar Option 1",
                        "Solar Option 2",
                    ],
                    load_data_options: [
                        "Load Option 1",
                        "Load Option 2",
                    ],
                }
            }
        },

        computed: {
            isInitial() {
                return this.currentStatus === STATUS_INITIAL;
            },
            isSaving() {
                return this.currentStatus === STATUS_SAVING;
            },
            isSuccess() {
                return this.currentStatus === STATUS_SUCCESS;
            },
            isFailed() {
                return this.currentStatus === STATUS_FAILED;
            }
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.input_data = this.$store.state.frontend_state[this.model_page_name]
            }
        },

        beforeDestroy() {
            this.save_page()
            this.save_page_server()
        },

        methods: {
            save_page() {
                let payload = {
                    model_page_name: this.model_page_name,
                    data: this.input_data
                };
                this.$store.commit('save_page', payload)
            },

            save_page_server() {
                let data = [];
                for(var i = 0; i < this.input_data.length; i++) {
                    data.push({
                        "name": this.input_data[i].name,
                        "value": this.input_data[i].value
                    })
                }
                let payload = {
                    model_page_name: this.model_page_name,
                    data: data,
                };
                this.$store.commit('save_server_page', payload)
            },

            add_solar_source() {

            },

            add_load_source() {

            },

            reset() {
            //    reset form to inital state
                this.currentStatus = STATUS_INITIAL;
                this.uploadedFiles = [];
                this.uploadError = null;
            },

            save(formData) {
            //    Upload data to the server
                this.currentStatus = STATUS_SAVING;

                upload(formData)
                    .then( x => {
                        this.uploadedFiles = [].concat(x);
                        this.currentStatus = STATUS_SUCCESS;
                    })
                    .catch(err => {
                        this.uploadError = err.response;
                        this.currentStatus = STATUS_FAILED;
                    });

            },

            filesChange(fieldName, fileList) {
            //    Handle file changes
                const formData = new FormData();

                if(!fileList.length) return;

            //    Append the files to formData
                Array
                    .from(Array(fileList.length).keys())
                    .map(x => {
                        formData.append(fieldName, fileList[x], fileList[x].name);
                    });

            //    Save it
                this.save(formData);
            }
        },

        mounted() {
            this.reset();
        }
    }
</script>

<style scoped>

</style>