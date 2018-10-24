<template>
    <div>
        <h1>{{ view_name }}</h1>
        <form>
            <input v-model="inputOne">
            <input v-model="inputTwo">
        </form>
        <br>
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
        name: "Tariffs",
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
    }
</style>