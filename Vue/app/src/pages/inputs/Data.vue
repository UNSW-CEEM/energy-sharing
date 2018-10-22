<template>
    <div>
        <h1>This View is named {{ view_name }}</h1>
        <ul>
            <li
                v-for="ex in examples"
                :key="ex.id">
                <span class="name">{{ ex.name }}, ${{ ex.price }}</span>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: "Data",
        data () {
            return {
                view_name: this.$options.name,
            }
        },
        computed: {
            examples() {
                return this.$store.state.examples
            }
        }
    }
</script>

<style scoped>

</style>