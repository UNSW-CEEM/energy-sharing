<template>
    <div>
        <h1>{{ view_name }}</h1>
        <button @click="sendSavedState()">Send Saved State</button>
    </div>
</template>

<script>
    export default {
        name: "Review",
        data () {
            return {
                view_name: this.$options.name,
                isConnected: false,
            }
        },
        sockets: {

        },
        methods: {
            sendSavedState() {
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