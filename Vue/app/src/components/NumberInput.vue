<template>
    <div>
        <input v-model="output_field" type="number">
    </div>
</template>

<script>
    import { required } from 'vuelidate/lib/validators';

    export default {
        name: "NumberInput",
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
            input_type: {
                default: "number"
            },
        },

        data() {
            return {
                this_name: this.$options.name,
            }
        },

        computed: {
            output_field: {
                get () {
                    return this.$store.state.output_data[this.input_page][this.field_name]
                },

                set(value) {
                    let payload = {
                        value: value,
                        input_page: this.input_page,
                        field_name: this.field_name,
                    };
                    this.$store.commit('setValue', payload)
                }
            }
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