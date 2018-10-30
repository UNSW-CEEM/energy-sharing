<template>
    <div>
        <p v-if="isConnected">We are connected to Flask Sockets!</p>
        <p> Message received: {{ socketMessage }}</p>
        <button @click="pingServer()">Ping Server</button>
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
            connect() {
                this.isConnected = true;
            },

            disconnect() {
                this.isConnected = false;
            },

            messageChannel(data) {
                this.socketMessage = data;
            }
        },

        methods: {
            pingServer() {
                console.log("Attempted to ping server. Connection status: ", this.isConnected)
                this.$socket.emit('pingServer', 'PING!')
            }
        }
    }
</script>

<style scoped>

</style>