<template>
    <div>
        <h1>This View is named {{ view_name }}</h1>
        <ul>
            <li
                v-for="ex in examples"
                :key="ex.id">
                <span class="name">{{ ex.name }}</span>
            </li>
            <li
                v-for="ex in examplesGetter"
                :key="ex.id">
                <span class="name">{{ ex.name }}</span>
            </li>
        </ul>
    </div>
</template>

<script>
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
            examplesGetter() {
                return this.$store.getters.examplesGetter;
            }
        }
    }
</script>

<style scoped>

</style>