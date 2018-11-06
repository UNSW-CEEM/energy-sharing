<template>
    <div>
        <p v-if="isConnected">We are connected to Flask Sockets!</p>
        <p> Message received: {{ socketMessage }}</p>
        <button @click="pingServer()">Ping Server</button>
        <button @click="exampleJSON()">Send Output Data State to Server</button>
    </div>
</template>

<script>
    export default {
        name: "SocketsTester",
        data() {
            return {
                isConnected: false,
                socketMessage: ''
            }
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
            }
        }
    }
</script>

<style scoped>

</style>