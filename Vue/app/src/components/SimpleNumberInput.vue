<template>
    <input
        class="my_input"
        v-bind:value="value"
        v-on:input="$emit('input', $event.target.value)"
        :placeholder="my_placeholder"
    >
</template>

<script>
    export default {
        name: "SimpleNumberInput",
        props: ["value", "my_placeholder"],

        data() {
            return {

            }
        },
    }
</script>

<style scoped>

    .my_input {
        text-align: center;
    }

</style>