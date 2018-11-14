<template>
    <div>
        <h1>{{ view_name }}</h1>
        <table>
            <tr>
                <th
                    v-for="header in table_headers"
                    :key="header.id"
                    :value="header.name">{{ header.name }}</th>
            </tr>
            <tr
                v-for="row in table_rows"
                :key="row.id">
                <td
                    v-for="input in row.inputs"
                    :key="input.id"
                    :is="input.tag">{{ input.name }}</td>
            </tr>
            <button @click="add_row()">Add Row</button>
        </table>
    </div>
</template>

<script>
    import DropdownInput from '@/components/DropdownInput.vue';
    import NumberInput from '@/components/NumberInput.vue';

    export default {
        name: "Financing",

        components: {
            DropdownInput,
            NumberInput,
        },

        data () {
            return {
                view_name: this.$options.name,
                table_headers: this.$store.state.input_data["model_finance"]["table_headers"],
            }
        },

        computed: {
            table_rows: {
                get () {
                    return this.$store.state.output_data["model_finance"]["table_rows"]
                }
            }
        },

        methods: {
            add_row() {
                let payload = {
                    row: {
                        inputs: [
                            {id: 0, name: "comp", tag: "NumberInput"},
                            {id: 1, name: "capex", tag: "NumberInput"},
                            {id: 2, name: "whopays", tag: "DropdownInput"},
                            {id: 3, name: "Discount Rate", tag: "NumberInput"},
                            {id: 4, name: "Amortization", tag: "NumberInput"},
                            {id: 5, name: "OPEX", tag: "NumberInput"},
                            {id: 6, name: "Who Pays", tag: "DropdownInput"},
                        ]
                    },
                    input_page: "model_finance",
                    field_name: "table_rows",
                };
                this.$store.commit('addRow', payload)
            }
        }
    }
</script>

<style scoped>

</style>