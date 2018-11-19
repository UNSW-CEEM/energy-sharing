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
        name: "Tariffs",

        components: {
            SimpleNumberInput,
            SimpleDropdown
        },

        data () {
            return {
                view_name: this.$options.name,
                model_page_name: "model_tariffs",

                table_headers: [
                    {header_id: 0, name: "tariff_name", additional_text:"Name"},
                    {header_id: 1, name: "fit_input", additional_text:"$"},
                    {header_id: 2, name: "peak_price", additional_text:"$"},
                    {header_id: 3, name: "shoulder_price", additional_text:"$"},
                    {header_id: 4, name: "off_peak_price", additional_text:"$"},
                ],
                table_rows: []
            }
        },

        computed: {

        },

        created() {
            if (this.model_page_name in this.$store.state.frontend_state) {
                this.table_rows = this.$store.state.frontend_state[this.model_page_name]
            } else {
                this.add_row()
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
                            col_id: 0,
                            field_name:"tariff_name",
                            tag:"my_number",
                            value:"",
                            placeholder:"Name",
                        },
                        {
                            col_id: 1,
                            field_name:"fit_input",
                            tag:"my_number",
                            value:"",
                            placeholder:"$"
                        },
                        {
                            col_id: 2,
                            field_name:"peak_price",
                            tag:"my_number",
                            value:"",
                            placeholder:"$",
                        },
                        {
                            col_id: 3,
                            field_name:"shoulder_price",
                            tag:"my_number",
                            value:"",
                            placeholder:"$",
                        },
                        {
                            col_id: 4,
                            field_name:"off_peak_price",
                            tag:"my_number",
                            value:"",
                            placeholder:"$",
                        },
                    ]
                };

                this.table_rows.push(new_row);
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
    .noBullets {
        list-style: none;
    }
</style>