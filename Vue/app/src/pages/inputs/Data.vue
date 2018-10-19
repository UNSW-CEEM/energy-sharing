<template>
    <h1>This View is named {{ view_name }}</h1>
</template>

<script>
    export default {
        name: "Data",
        data () {
            return {
                view_name: this.$options.name,
            }
        }
    }
</script>

<style scoped>

</style>