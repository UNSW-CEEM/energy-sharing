<template>
    <select
            v-bind:value="value"
            v-on:input="$emit('input', $event.target.value)">
        <option value="" disabled selected hidden>{{ my_placeholder }}</option>
        <option
            v-for="option in my_options"
            :value="option">
            {{ option }}
        </option>
    </select>
</template>

<script>
    import { required } from 'vuelidate/lib/validators';

    export default {
        name: "DropdownInput",
        props: ["value", "my_options", "my_placeholder"],

        data () {
            return {

            }
        }
    }
</script>

<style scoped>

</style>