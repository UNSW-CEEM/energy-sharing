<template>
    <div>
        <h1>{{ view_name }}</h1>
        <table>
            <tr>
                <th
                    v-for="header in table_headers"
                    :key="header.header_id"
                    :value="header.name">{{ header.name }}</th>
            </tr>
            <tr
                v-for="row in table_rows"
                :key="row.row_id">
                <td v-for="input in row.row_inputs"
                :key="input.col_id"
                >
                    <!-- If a simple input use this component.-->
                    <SimpleNumberInput v-if="input.tag==='my_number'" v-model="input.value"/>
                    <!-- If a dropdown use this component.-->
                    <SimpleDropdown v-else-if="input.tag==='my_dropdown'"
                                    v-model="input.value"
                                    :my_options="my_options[input.dropdown_key]"/>
                </td>
            </tr>
            <button @click="add_row()">Add Row</button>
        </table>
    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';
    import SimpleDropdown from '@/components/SimpleDropdown.vue';

    export default {
        name: "Financing",

        components: {
            SimpleNumberInput,
            SimpleDropdown
        },

        data () {
            return {
                view_name: this.$options.name,
                model_name: "model_finance",

                table_headers: [
                    {id: 0, name: "Component"},
                    {id: 1, name: "CAPEX"},
                    {id: 2, name: "Who Pays"},
                    {id: 3, name: "Discount Rate"},
                    {id: 4, name: "Amortization"},
                    {id: 5, name: "OPEX"},
                    {id: 6, name: "Who Pays"},
                ],

                table_rows: [],

                my_options: {
                    example: {
                        option_one: "Option One",
                        option_two: "Option Two",
                    },
                    who_pays: {
                        option_one: "Option 1",
                        option_two: "Option 2",
                    }
                },
            }
        },

        computed: {

        },

        created() {
            this.add_row()
        },

        methods: {
            add_row() {
                let array_length = this.table_rows.length;
                let new_row = {
                    row_id: array_length,
                    row_inputs: [
                        {id: 0, text: "Comp", name: "comp", tag: "my_number", value:""},
                        {id: 1, text: "CAP", name: "capex", tag: "my_number", value:""},
                        {id: 2, text: "CAP PAY", name: "capex_payer", tag: "my_dropdown", value:"", dropdown_key:"who_pays"},
                        {id: 3, text: "DISC RAT", name: "discount_rate", tag: "my_number", value:""},
                        {id: 4, text: "AMORT", name: "amortization", tag: "my_number", value:""},
                        {id: 5, text: "OPEX", name: "opex", tag: "my_number", value:""},
                        {id: 6, text: "OP PAY", name: "opex_payer", tag: "my_dropdown", value:"", dropdown_key:"example"},
                    ]
                };

                this.table_rows.push(new_row);
            }
        }
    }
</script>

<style scoped>

</style>