<template>
    <div>
        <h1>{{ view_name }}</h1>
        <form>
        </form>
    </div>
</template>

<script>
    import { mapFields } from 'vuex-map-fields';

    export default {
        name: "Tariffs",
        data () {
            return {
                view_name: this.$options.name,
            }
        },
        computed: {
            ...mapFields({

            }),
        },
        methods: {

        }
    }
</script>

<style scoped>
    .noBullets {
        list-style: none;
    }
</style>