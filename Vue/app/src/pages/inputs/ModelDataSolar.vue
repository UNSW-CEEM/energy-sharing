<template>
    <div class="background">
        <div class="main-container">
            <h1 id="solar-title" class="solar-title">Solar Files</h1>
            <ul>
                <li v-for="(file, index) in solar_files" :key="file.id">
                    <span>{{file.name}}</span> -
                    <span>{{file.size}}</span> -
                    <span v-if="file.error">{{file.error}}</span>
                    <span v-else-if="file.success">success</span>
                    <span v-else-if="file.active">active</span>
                    <span v-else-if="file.active">active</span>
                    <span v-else></span>
                </li>
            </ul>
            <div>
                <file-upload
                    class="solar_upload"
                    post-action="http://localhost:5000/upload/solar_data"
                    extensions="gif,jpg,jpeg,png,webp, csv"
                    accept="image/png,image/gif,image/jpeg,image/webp, text/csv"
                    :multiple="true"
                    :size="1024 * 1024 * 10"
                    v-model="solar_files"
                    @input-filter="inputFilter"
                    @input-file="inputFile"
                    ref="upload">
                    <button class="solar-file-button">Select files</button>
                </file-upload>
                <button v-if="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true">
                    Start Upload
                </button>
                <button v-else @click.prevent="$refs.upload.active = false">
                    Stop Upload
                </button>
            </div>
            <div class="solar-files-list-container">
                <ul class="solar-files-list">
                    <li v-for="item in files_lists.solar_files_list">{{ item }}</li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
    // Note this is adapted from:
    // "https://github.com/lian-yue/vue-upload-component/blob/master/docs/views/examples/Simple.vue"

    import FileUpload from 'vue-upload-component';

    export default {
        name: "ModelDataSolar",
        components: {
            FileUpload
        },

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "SolarUpload",
                is_connected: false,

                files_lists: {
                    solar_files_list: [],
                    load_files_list: [],
                },
                solar_files: [],
            }
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.input_data = this.$store.state.frontend_state[this.model_page_name]
            }
            this.get_solar_files();
            this.get_load_files();
        },

        methods: {

            get_solar_files() {
                this.$socket.emit('get_solar_files')
            },

            get_load_files() {
                this.$socket.emit('get_load_files')
            },

            inputFilter(newFile, oldFile, prevent) {
                if (newFile && !oldFile) {
                    // Before adding a file
                    // Filter system files or hide files
                    if (/(\/|^)(Thumbs\.db|desktop\.ini|\..+)$/.test(newFile.name)) {
                        return prevent()
                    }
                    // Filter php html js file
                    if (/\.(php5?|html?|jsx?)$/i.test(newFile.name)) {
                        return prevent()
                    }
                }
            },

            inputFile(newFile, oldFile) {
                if (newFile && !oldFile) {
                    // add
                    console.log('add', newFile)
                }
                if (newFile && oldFile) {
                    // update
                    this.get_solar_files()
                    console.log('update', newFile)
                }
                if (!newFile && oldFile) {
                    // remove
                    console.log('remove', oldFile)
                }
            }
        },

        sockets: {
            filesChannel: function(response) {
                this.is_connected = true;
                this.files_lists[response.key] = response.data;
            },
        }
    }
</script>

<style scoped>
    .main-container {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: start;
        animation-name: fade-in;
        animation-duration: 1s;
    }

    .solar-title {
        width: 100%;
    }

    .solar-file-button {

    }

    .solar-files-list-container {
        display: flex;
        justify-content: space-between;
    }

    .solar-files-list {
        width: 100%;
    }

</style>