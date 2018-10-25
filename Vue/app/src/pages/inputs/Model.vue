<template>
    <div>
        <h1>This View is named {{ view_name }}</h1>
        <form>
            <select v-model="simulation">
                <option value="Simulation Type 1">Simulation Type 1</option>
                <option value="Simulation Type 2">Simulation Type 2</option>
                <option value="Simulation Type 3">Simulation Type 3</option>
            </select>
            <select v-model="network_type">
                <option value="Network Type 1">Network Type 1</option>
                <option value="Network Type 2">Network Type 2</option>
                <option value="Network Type 3">Network Type 3</option>
            </select>
        </form>
    </div>
</template>

<script>
    import { mapActions, mapGetters } from 'vuex';
    import { mapFields } from 'vuex-map-fields';

    export default {
        name: "Model",
        data () {
            return {
                view_name: this.$options.name,
            }
        },
        computed: {
            ...mapFields({
                simulation: 'saved_data.model.simulation',
                network_type: 'saved_data.model.network_type',
            }),
        },
        methods: {

        }
    }
</script>

<style scoped>

</style>