<template>
    <div>
        <p v-if="isConnected">We are connected to Flask Sockets!</p>
        <p> Message received: {{ socketMessage }}</p>
        <button @click="pingServer()">Ping Server</button>
        <button @click="exampleJSON()">Send Output Data State to Server</button>
        <button @click="get_solar_files()">Test Get Solar Files</button>
        <button @click="get_load_files()">Test Get Load Files</button>
        <button @click="run_model()">Run Model</button>
        <ul> Solar Files
            <li v-for="file in filesList.solar_files_list">{{ file }}</li>
        </ul>
        <ul> Load Files
            <li v-for="file in filesList.load_files_list">{{ file }}</li>
        </ul>

        <!--Test stuff-->
        <div v-if="!my_file">
            <h2>Select a File</h2>
            <input type="file" @change="onFileChange"/>
        </div>
        <div v-else>
            <button @click="removeFile">Remove file</button>
            <p>{{ my_file }}</p>
            <!--<img :src="my_file"/>-->
        </div>
    </div>
</template>

<script>
    export default {
        name: "SocketsTester",
        data() {
            return {
                my_file:'',

                isConnected: false,
                socketMessage: '',
                filesList: {
                    solar_files_list: [],
                    load_files_list: [],
                },
            }
        },

        computed: {
            
        },

        sockets: {
            connect: function() {
                console.log("This client connected");
                this.isConnected = true;
            },

            disconnect: function() {
                this.isConnected = false;
            },

            messageChannel: function(data) {
                console.log("Message channel received: ", data);
                this.isConnected = true;
                this.socketMessage = data;
            },

            filesChannel: function(response) {
                this.isConnected = true;
                this.filesList[response.key] = response.data;
            }
        },

        methods: {
            pingServer() {
                console.log("Attempted to ping server. Connection status: ", this.isConnected);
                this.$socket.emit('pingServer', 'PING!');
            },

            exampleJSON() {
                var this_data = this.$store.state.output_data;
                console.log("Sending some json: ", this_data);
                this.isConnected = true;
                this.$socket.emit('exampleJSON', this_data);
            },

            get_solar_files() {
                this.$socket.emit('get_solar_files')
            },

            get_load_files() {
                this.$socket.emit('get_load_files')
            },

            upload_test(data) {
                this.$socket.emit('upload_test', data)
            },

            // Tests
            onFileChange(e) {
                var files = e.target.files || e.dataTransfer.files;
                if (!files.length)
                    return;
                // this.createImage(files[0])
                this.saveFile(files[0])
            },


            saveFile(file) {
                var reader = new FileReader();
                var vm = this;

                reader.onload = (e) => {
                    vm.my_file = e.target.result;
                };
                reader.readAsDataURL(file);
            },

            createImage(file) {
                var my_file = new File();
                var reader = new FileReader();
                var vm = this;

                reader.onload = (e) => {
                    vm.my_file = e.target.result;
                };
                reader.readAsDataURL(file);

            },

            removeFile: function (e) {
                this.my_file = '';
            },

            run_model() {
                this.$socket.emit('run_model')
            }
        },

    }
</script>

<style scoped>

</style>