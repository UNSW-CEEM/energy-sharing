<template>
    <div>
        <h4> Progress: {{ completed_pages }}/{{ total_pages }} input pages completed.</h4>
    </div>
</template>

<script>
    export default {
        name: "ModelFooter",

        data() {
            return {

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

</style>