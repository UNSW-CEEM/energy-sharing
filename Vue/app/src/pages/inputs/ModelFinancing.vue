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
                model_page_name: "model_financing",

                table_headers: [
                    {id: 0, name: "Component", additional_text:"Name"},
                    {id: 1, name: "CAPEX", additional_text:"$"},
                    {id: 2, name: "Who Pays", additional_text:"Who"},
                    {id: 3, name: "Discount Rate", additional_text:"%"},
                    {id: 4, name: "Amortization", additional_text:"years"},
                    {id: 5, name: "OPEX", additional_text:"$"},
                    
                ],

                table_rows: [],

                my_options: {
                    
                    who_pays: {
                        option_one: "Retailer",
                        option_two: "TNSP",
                        option_three: "DNSP",
                        option_four: "Scheme Operator",
                        option_five: "Participants",
                    }
                },
            }
        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.table_rows = this.$store.state.frontend_state[this.model_page_name]
            } else {
                this.populate_rows()
            }
        },

        beforeDestroy() {
            this.save_page()
            this.save_page_server()
        },

        methods: {
            add_row() {
                let array_length = this.table_rows.length;
                let new_row = {
                    row_id: array_length,
                    row_inputs: [
                        {
                            id: 0,
                            name: "component",
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
                       
                    ]
                };

                this.table_rows.push(new_row);
            },

            populate_rows() {
                var components = ["Central Solar", "Central Battery"]
                for(var i = 0; i< components.length; i++){
                    let array_length = this.table_rows.length;
                    let new_row = {
                        row_id: array_length,
                        row_inputs: [
                            {
                                id: 0,
                                name: "component",
                                tag: "my_number",
                                value:components[i],
                                placeholder:"Name",
                            },
                            {
                                id: 1,
                                name: "capex",
                                tag: "my_number",
                                value: Number(Math.random() * 100000).toFixed(0),
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
                                value:7,
                                placeholder:"%",
                            },
                            {
                                id: 4,
                                name: "amortization",
                                tag: "my_number",
                                value:20,
                                placeholder:"Years",
                            },
                            {
                                id: 5,
                                name: "opex",
                                tag: "my_number",
                                value:0,
                                placeholder:"$",
                            },
                            
                        ]
                    };

                    this.table_rows.push(new_row);
                }
            },

            save_page() {
                let payload = {
                    model_page_name: this.model_page_name,
                    data: this.table_rows
                };
                this.$store.commit('save_page', payload)
            },

            save_page_server() {
                let data = [];

                for(var i = 0; i < this.table_rows.length; i++) {
                    let row = this.table_rows[i].row_inputs;
                    let row_data = []

                    for( var j = 0; j < row.length; j++) {
                        row_data.push({
                            "name": row[j].name,
                            "value": row[j].value
                        })
                    }
                    data.push({
                        row_id: i,
                        row_inputs: row_data
                    })
                }

                let payload = {
                    model_page_name: this.model_page_name,
                    data: data,
                };
                this.$store.commit('save_server_page', payload)
            },
        }
    }
</script>

<style scoped>

h1{
    animation-name: fade-in;
    animation-duration: 2s;
}

table{
    animation-name: fade-in;
    animation-duration: 2s;
}

</style>