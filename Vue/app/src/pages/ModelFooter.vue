<template>
    <div>
        <div class="status" v-if="!sleeping"> Status: {{ status }}</div>
    </div>
</template>

<script>
    export default {
        name: "ModelFooter",

        data() {
            return {
                is_connected: false,
                sleeping: true,
                status: "",
            }
        },

        sockets: {
            status_channel: function (response) {
                this.is_connected = true;
                this.sleeping = false;
                this.status = response.data.message;
            }
        },

        computed: {
            completed_pages: {
                get() {
                    return this.$store.state.frontend_state.completed_pages;
                }
            },
            total_pages: {
                get() {
                    return this.$store.state.frontend_state.total_pages;
                }
            }
        },

        methods: {

        }
    }
</script>

<style scoped>
.status{
    display:flex;
    flex-direction:row;
    justify-content: center;
    align-items: center;
    width:100%;
    height:100%;
}
</style>