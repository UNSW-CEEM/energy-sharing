<template>
    <div class="main-container">
        <h1 class="page-heading">{{ view_name }}</h1>
        <div class="list-container">
            <div class="solar-files">
                <h1>Solar Files</h1>
                <ul>
                    <li v-for="item in files_lists.solar_files_list">{{ item }}</li>
                </ul>
                <button @click="add_solar_source">Add Solar File</button>
            </div>
            <div class="load-files">
                <h1>Load Files</h1>
                <ul>
                    <li v-for="item in files_lists.load_files_list">{{ item }}</li>
                </ul>
                <button @click="add_load_source">Add Load File</button>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Data",

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "model_data",
                is_connected: false,

                files_lists: {
                    solar_files_list: [],
                    load_files_list: [],
                }
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
        background-color: white;
    }

span{
    animation-name: fade-in;
    animation-duration: 2s;
}
</style>