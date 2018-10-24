<template>
    <div>
        <h1>{{ view_name }}</h1>
        <h4>Below Are Inputs For Store</h4>
        <form>
            <input v-model="inputOne">
            <input v-model="inputTwo">
        </form>
        <br>
        <h4>Below Shows Value In Store</h4>
        <ul class="noBullets">
            <li>
                <span>{{inputOne}}</span>
            </li>
            <li>
                <span>{{inputTwo}}</span>
            </li>
        </ul>
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
                inputOne: 'example_inputs[0].value',
                inputTwo: 'example_inputs[1].value',
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