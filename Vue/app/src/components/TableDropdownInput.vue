<template>
    <div>
        <select v-model="output_field">
            <option value="" disabled selected hidden>{{ placeholder }}</option>
            <option
                v-for="input in input_fields"
                :key="input.id"
                :value="input.name">
                {{ input.name }}
            </option>
        </select>
    </div>
</template>

<script>
    import { required } from 'vuelidate/lib/validators';

    export default {
        name: "DropdownInput",
        props: {
            field_name: {
                default: "default_value"
            },
            input_page: {
                default: "default_value"
            },
            placeholder: {
                default: "Override your placeholder"
            },
            array_name: {
                default: "default_value"
            },
            row_index: {
                default: "default_value"
            }
        },

        data() {
            return {
                this_name: this.$options.name,
                input_fields: this.$store.state.input_data[this.input_page][this.field_name]
            }
        },

        computed: {
            output_field: {
                get () {
                    return this.$store.state.output_data[this.input_page][this.array_name][this.row_index][this.field_name]
                },

                set(value) {
                    let payload = {
                        value: value,
                        input_page: this.input_page,
                        field_name: this.field_name,
                        array_name: this.array_name,
                        row_index: this.row_index
                    };
                    this.$store.commit('setTableDropdown', payload)
                }
            }
        },

        methods: {

        },

        validations: {
            output_field: {
                required,
            }
        }
    }
</script>

<style scoped>

</style>