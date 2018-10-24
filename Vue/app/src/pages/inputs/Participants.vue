<template>
    <div>
        <h1>{{ view_name }}</h1>
        <button @click="show_which = 'DynamicOne'">Show Component One</button>
        <button @click="show_which = 'DynamicTwo'">Show Component Two</button>

        <component :is="show_which"></component>
    </div>
</template>

<script>
    import DynamicOne from '@/components/DynamicOne.vue';
    import DynamicTwo from '@/components/DynamicTwo.vue';

    export default {
        name: "Participants",
        components: {
            DynamicOne,
            DynamicTwo
        },
        data () {
            return {
                view_name: this.$options.name,
                show_which: 'DynamicOne'
            }
        }
    }
</script>

<style scoped>

</style>