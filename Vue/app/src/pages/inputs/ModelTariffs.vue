<template>
    <div>
        <h1>{{ view_name }}</h1>
        <table style="width:100%">
            <!--Headers added from table_headers array-->
            <tr>
                <th v-for="header in table_headers"
                :key="header.header_id"
                :value="header.name">{{ header.name }}</th>
            </tr>
            <!--Rows added for each item in table_rows array-->
            <tr v-for="row in table_rows"
            :key="row.row_id">
                <!--Fields added for each column in each row-->
                <td v-for="input in row.row_inputs"
                :key="input.col_id"
                >
                    <SimpleNumberInput v-model="input.value"/>
                </td>
            </tr>
            <button @click="add_row()">Add Row</button>
        </table>
    </div>
</template>

<script>
    import SimpleNumberInput from '@/components/SimpleNumberInput.vue';

    export default {
        name: "Tariffs",

        components: {
            SimpleNumberInput
        },

        data () {
            return {
                view_name: this.$options.name,
                table_headers: [
                    {header_id: 0, name: "tariff_name"},
                    {header_id: 1, name: "fit_input"},
                    {header_id: 2, name: "peak_price"},
                    {header_id: 3, name: "shoulder_price"},
                    {header_id: 4, name: "off_peak_price"},
                ],
                table_rows: []
            }
        },

        computed: {

        },

        created() {
            this.add_row()
        },

        methods: {
            add_row() {
                var array_length = this.table_rows.length;
                let new_row = {
                    row_id:array_length,
                    row_inputs: [
                        {col_id: 0, field_name:"tariff_name", tag:"input", value:""},
                        {col_id: 1, field_name:"fit_input", tag:"input", value:""},
                        {col_id: 2, field_name:"peak_price", tag:"input", value:""},
                        {col_id: 3, field_name:"shoulder_price", tag:"input", value:""},
                        {col_id: 4, field_name:"off_peak_price", tag:"input", value:""},
                    ]
                };
                this.table_rows.push(new_row);
            }
        }
    }
</script>

<style scoped>
    .noBullets {
        list-style: none;
    }
</style>