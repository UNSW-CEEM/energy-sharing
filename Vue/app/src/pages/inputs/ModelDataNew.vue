
<template>
    <div class="main-container">
        <h1 id="example-title" class="example-title">Simple Example</h1>
            <div class="upload">
            <ul>
                <li v-for="(file, index) in files" :key="file.id">
                    <span>{{file.name}}</span> -
                    <span>{{file.size | formatSize}}</span> -
                    <span v-if="file.error">{{file.error}}</span>
                    <span v-else-if="file.success">success</span>
                    <span v-else-if="file.active">active</span>
                    <span v-else-if="file.active">active</span>
                    <span v-else></span>
                </li>
            </ul>
            <div class="example-btn">
                <file-upload
                    class="btn btn-primary"
                    post-action="/upload/post"
                    extensions="gif,jpg,jpeg,png,webp"
                    accept="image/png,image/gif,image/jpeg,image/webp"
                    :multiple="true"
                    :size="1024 * 1024 * 10"
                    v-model="files"
                    @input-filter="inputFilter"
                    @input-file="inputFile"
                    ref="upload">
                    <i class="fa fa-plus"></i>
                    Select files
                </file-upload>
                <button type="button" class="btn btn-success" v-if="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true">
                    <!--<i class="fa fa-arrow-up" aria-hidden="true"></i>-->
                    Start Upload
                </button>
                <button type="button" class="btn btn-danger"  v-else @click.prevent="$refs.upload.active = false">
                    <!--<i class="fa fa-stop" aria-hidden="true"></i>-->
                    Stop Upload
                </button>
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
                model_page_name: "model_data",
                is_connected: false,

                files_lists: {
                    solar_files_list: [],
                    load_files_list: [],
                },
                files: [],
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
                console.log("This client connected");
                this.is_connected = true;
            },

            disconnect: function() {
                this.is_connected = false;
            },

            filesChannel: function(response) {
                console.log("received response: ", response);
                this.is_connected = true;
                this.files_lists[response.key] = response.data;
            },
        }
    }
</script>

<style scoped>
    .main-container {
        display: flex;
        justify-content: flex-start;
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

    .upload {

    }

    /*.example-simple label.btn {*/
        /*margin-bottom: 0;*/
        /*margin-right: 1rem;*/
    /*}*/

    span {
        animation-name: fade-in;
        animation-duration: 2s;
    }
</style>