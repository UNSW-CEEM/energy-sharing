<template>
    <div>
        <h1>{{ view_name }}</h1>
        <h4>Below Are Inputs For Store</h4>
        <form>
            <p>Sharing Algorithm:</p>
            <select v-model="sharing_algorithm">
                <option value="" disabled selected hidden>Select Your Sharing Algorithm</option>
                <option value="Algorithm 0">Algorithm 0</option>
                <option value="Algorithm 1">Algorithm 1</option>
                <option value="Algorithm 2">Algorithm 2</option>
                <option value="Algorithm 3">Algorithm 3</option>
            </select>
            <br>
            <p>Scaling Factor:</p>
            <input placeholder="Enter Your Scaling Factor">
            <br>
            <p>Select Your Data Source</p>
            <select v-model="data_source">
                <option value="" disabled selected hidden>Select Your Data Source</option>
                <option
                    v-for="source in input_data_source"
                    :key="source.id"
                    :value="source.name">
                    {{ source.name }}
                </option>
            </select>
        </form>
    </div>
</template>

<script>
    import { mapFields } from 'vuex-map-fields';

    export default {
        name: "CentralSolar",

        data () {
            return {
                view_name: this.$options.name,
            }
        },
        computed: {
            ...mapFields({
                sharing_algorithm: 'saved_data.central_solar.sharing_algorithm',
                data_source: 'saved_data.central_solar.data_source',
                input_data_source: 'inputs_data.central_solar.data_source',
            }),
        },
        methods: {

        }
    }
</script>

<style scoped>
    .noBullets {
        list-style: none;
        background: white;
        margin: 10px;
    }


</style>