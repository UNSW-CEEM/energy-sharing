<template>
    <div>
        <h1>{{ child_store }}</h1>
        <select v-model="output_field">
            <option value="" disabled selected hidden>{{ this_placeholder }}</option>
            <option
                v-for="source in input_fields"
                :key="source.id"
                :value="source.name">
                {{ source.name }}
            </option>
        </select>
    </div>
</template>

<script>
    import { mapFields } from 'vuex-map-fields';

    export default {
        name: "DropdownInput",
        props: {
            child_store: {
                default: "default_value"
            },
            parent_store: {
                default: "default_value"
            },
            placeholder: {
                default: "default_value"
            }
        },

        data() {
            return {
                this_name: this.$options.name,
                // I think these are pointless
                this_parent_store: this.parent_store,
                this_child_store: this.child_store,
                this_placeholder: this.placeholder,
            }
        },
        computed: {
            ...mapFields({
                // input_fields: 'inputs_data.central_solar.data_source',
                input_fields: ["inputs_data", this.parent_store, this.child_store].join('.'),
                output_field: 'saved_data.central_solar.data_source',
            })
        }
    }
</script>

<style scoped>

</style>