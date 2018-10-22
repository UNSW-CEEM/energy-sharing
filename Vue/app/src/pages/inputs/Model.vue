<template>
    <div>
        <h1>This View is named {{ view_name }}</h1>
        <ul>
            <li
                v-for="ex in examplesGetter"
                :key="ex.id">
                <span class="name">{{ ex.name }}, ${{ ex.price }}</span>
            </li>
            <button v-on:click="reducePrice(10)">Reduce Price</button>
        </ul>
    </div>
</template>

<script>
    import { mapActions } from 'vuex';
    import { mapGetters } from 'vuex';

    export default {
        name: "Model",
        data () {
            return {
                view_name: this.$options.name,
            }
        },
        computed: {
            examples() {
                return this.$store.state.examples;
            },
            ...mapGetters([
                'examplesGetter',
            ])
        },
        methods: {
            ...mapActions([
                'reducePrice'
            ])
        }
    }
</script>

<style scoped>

</style>