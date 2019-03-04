<template>
    <div class="main-container">
        <div class="load-container">
            <h1 id="load-title" class="load-title">Load Files</h1>
            <ul>
                <li v-for="(file, index) in load_files" :key="file.id">
                    <span>{{file.name}}</span> -
                    <span>{{file.size | formatSize}}</span> -
                    <span v-if="file.error">{{file.error}}</span>
                    <span v-else-if="file.success">success</span>
                    <span v-else-if="file.active">active</span>
                    <span v-else-if="file.active">active</span>
                    <span v-else></span>
                </li>
            </ul>
            <div>
                <file-upload
                    class="load_upload"
                    post-action="http://localhost:5000/upload/load_data"
                    extensions="gif,jpg,jpeg,png,webp, csv"
                    accept="image/png,image/gif,image/jpeg,image/webp, text/csv"
                    :multiple="true"
                    :size="1024 * 1024 * 10"
                    v-model="load_files"
                    @input-filter="inputFilter"
                    @input-file="inputFile"
                    ref="upload">
                    <button>Select files</button>
                </file-upload>
                <button v-if="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true">
                    Start Upload
                </button>
                <button v-else @click.prevent="$refs.upload.active = false">
                    Stop Upload
                </button>
            </div>
            <div class="load-files">
                <ul>
                    <li v-for="item in files_lists.load_files_list">{{ item }}</li>
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
        name: "Data",
        components: {
            FileUpload
        },

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "LoadUpload",
                is_connected: false,

                files_lists: {
                    solar_files_list: [],
                    load_files_list: [],
                },
                load_files: [],
            }
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.input_data = this.$store.state.frontend_state[this.model_page_name]
            }
            this.get_solar_files();
            this.get_load_files();
        },

        beforeDestroy() {

        },

        methods: {

            add_solar_source() {
                console.log("Implement Me");
            },

            add_load_source() {
                console.log("Implement Me");
            },

            get_solar_files() {
                console.log("Getting solar files")
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
            connect: function() {
                this.is_connected = true;
            },

            disconnect: function() {
                this.is_connected = false;
            },

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
    }

    .load_upload {
        color: white;
    }

    .list-container {
        display: flex;
        justify-content: space-between;
        animation-name: fade-in;
        animation-duration: 2s;
    }

    .solar-files {
        width: 50%;
    }

    .load-files {
        width: 50%;
    }

    .page-heading {
        width: 100%;
        animation-name: fade-in;
        animation-duration: 2s;
    }

    span {
        animation-name: fade-in;
        animation-duration: 2s;
    }
</style>