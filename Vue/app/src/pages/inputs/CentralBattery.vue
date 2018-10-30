<!--FOCUS ON ME AND MY COMPONENTS-->
<template>
    <div>
        <h1>{{ view_name }}</h1>
        <DropdownInput
            field_name="dispatch_algorithm"
            input_page="central_battery"
            placeholder="Select your data source" />
        <DropdownInput
            field_name="data_source"
            input_page="central_solar"/>
        <NumberInput
        field_name="capacity"
        input_page="central_battery"/>
    </div>
</template>

<script>
    import DropdownInput from '@/components/DropdownInput.vue';
    import NumberInput from '@/components/NumberInput.vue';

    export default {
        name: "CentralBattery",
        components: {
            DropdownInput,
            NumberInput,
        },

        data () {
            return {
                view_name: this.$options.name,
            }
        },

    }
</script>

<style scoped>

</style>