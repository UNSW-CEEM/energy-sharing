<template>
    <div>
        <h1>{{ view_name }}</h1>
        <p>{{ this_parent }}</p>
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
                    :is="input.tag"
                    :placeholder="input.name"
                    :field_name="input.name"
                    :input_page="model_name"
                    :array_name="'table_rows'"
                    :row_index="row.id">{{ input.text }}</td>
            </tr>
            <button @click="add_row()">Add Row</button>
        </table>
    </div>
</template>

<script>
    import TableDropdownInput from '@/components/TableDropdownInput.vue';
    import NumberInput from '@/components/NumberInput.vue';

    export default {
        name: "Financing",

        components: {
            TableDropdownInput,
            NumberInput,
        },

        data () {
            return {
                view_name: this.$options.name,
                this_parent: this.$parent.$options.name,
                model_name: "model_finance",
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
                        row_id: 0,
                        inputs: [
                            {id: 0, text: "Comp", name: "comp", tag: "NumberInput"},
                            {id: 1, text: "CAP", name: "capex", tag: "NumberInput"},
                            {id: 2, text: "CAP PAY", name: "capex_payer", tag: "TableDropdownInput"},
                            {id: 3, text: "DISC RAT", name: "discount_rate", tag: "NumberInput"},
                            {id: 4, text: "AMORT", name: "amortization", tag: "NumberInput"},
                            {id: 5, text: "OPEX", name: "opex", tag: "NumberInput"},
                            {id: 6, text: "OP PAY", name: "opex_payer", tag: "TableDropdownInput"},
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