<template>
    <div>
      <!--UPLOAD-->
      <form enctype="multipart/form-data" novalidate v-if="isInitial || isSaving">
        <h1>Upload images</h1>
        <div class="dropbox">
          <input type="file" multiple :name="uploadFieldName" :disabled="isSaving" @change="filesChange($event.target.name, $event.target.files); fileCount = $event.target.files.length"
            accept="image/*" class="input-file">
            <p v-if="isInitial">
              Drag your file(s) here to begin<br> or click to browse
            </p>
            <p v-if="isSaving">
              Uploading {{ fileCount }} files...
            </p>
        </div>
      </form>
  </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';

    // Example
    import { upload, uploadTest } from "../../services/FileUpload";

    const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;
    // Example ^^

    export default {
        name: "Data",

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "model_data",

                // File service attempts
                uploadedFiles: [],
                uploadError: null,
                currentStatus: null,
                uploadFieldName: 'photos',
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

        methods: {

            reset() {
                this.currentStatus = STATUS_INITIAL;
                this.uploadedFiles = [];
                this.uploadError = null;
            },

            save(formData) {
            //    Upload data to the server
                this.currentStatus = STATUS_SAVING;

                console.log(formData)
                this.upload_test(formData)
                // upload(formData)
                //     .then( x => {
                //         this.uploadedFiles = [].concat(x);
                //         this.currentStatus = STATUS_SUCCESS;
                //     })
                //     .catch(err => {
                //         this.uploadError = err.response;
                //         this.currentStatus = STATUS_FAILED;
                //     });
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
            },

            upload_test(data) {
                this.$socket.emit('upload_test', data);
            }
        },

        mounted() {
            this.reset();
        },
    }
</script>

<style scoped>

</style>