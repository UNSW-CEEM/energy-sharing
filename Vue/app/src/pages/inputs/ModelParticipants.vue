<!--FOCUS ON ME AND MY COMPONENTS-->
<template>
    <div>
        <h1>{{ view_name }}</h1>

    </div>
</template>

<script>

    export default {
        name: "Participants",
        components: {
        },
        data () {
            return {
                view_name: this.$options.name,
            }
        }
    }
</script>

<style scoped>

</style>