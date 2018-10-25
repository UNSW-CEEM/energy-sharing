<!--FOCUS ON ME AND MY COMPONENTS-->
<template>
    <div>
        <h1>{{ view_name }}</h1>
        <DropdownInput
            child_store="data_source"
            parent_store="central_solar" />
            <!--placeholder="Select your data source" -->
    </div>
</template>

<script>
    import DropdownInput from '@/components/DropdownInput.vue';

    export default {
        name: "CentralBattery",

        components: {
          DropdownInput
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