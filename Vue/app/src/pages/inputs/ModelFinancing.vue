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
            <tr>
                <td
                    v-for="header in table_headers"
                    :key="header.header_id">{{ header.additional_text }}</td>
            </tr>
            <tr
                v-for="row in table_rows"
                :key="row.row_id">
                <td v-for="input in row.row_inputs"
                :key="input.col_id"
                >
                    <!-- If a simple input use this component.-->
                    <SimpleNumberInput
                            v-if="input.tag==='my_number'"
                            v-model="input.value"
                            :my_placeholder="input.placeholder"/>
                    <!-- If a dropdown use this component.-->
                    <SimpleDropdown v-else-if="input.tag==='my_dropdown'"
                                    v-model="input.value"
                                    :my_options="my_options[input.dropdown_key]"
                                    :my_placeholder="input.placeholder"/>
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
                    {id: 0, name: "Component", additional_text:"Name"},
                    {id: 1, name: "CAPEX", additional_text:"$"},
                    {id: 2, name: "Who Pays", additional_text:"Who"},
                    {id: 3, name: "Discount Rate", additional_text:"%"},
                    {id: 4, name: "Amortization", additional_text:"years"},
                    {id: 5, name: "OPEX", additional_text:"$"},
                    {id: 6, name: "Who Pays", additional_text:"Who"},
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
                        {
                            id: 0,
                            name: "comp",
                            tag: "my_number",
                            value:"",
                            placeholder:"Name",
                        },
                        {
                            id: 1,
                            name: "capex",
                            tag: "my_number",
                            value:"",
                            placeholder:"$",
                        },
                        {
                            id: 2,
                            name: "capex_payer",
                            tag: "my_dropdown",
                            value:"",
                            dropdown_key:"who_pays",
                            placeholder:"Select Payer",
                        },
                        {
                            id: 3,
                            name: "discount_rate",
                            tag: "my_number",
                            value:"",
                            placeholder:"%",
                        },
                        {
                            id: 4,
                            name: "amortization",
                            tag: "my_number",
                            value:"",
                            placeholder:"Years",
                        },
                        {
                            id: 5,
                            name: "opex",
                            tag: "my_number",
                            value:"",
                            placeholder:"$",
                        },
                        {
                            id: 6,
                            name: "opex_payer",
                            tag: "my_dropdown",
                            value:"",
                            dropdown_key:"example",
                            placeholder:"Select Payer",
                        },
                    ]
                };

                this.table_rows.push(new_row);
            }
        }
    }
</script>

<style scoped>

</style>