<template>
    <div class="content">
        <h1>Contact Us</h1>
        <p>
            <ul class="noBullets">
                    <li>Email: {{email}}</li>
                    <li>Website: {{web}}</li>
            </ul>
        </p>
    </div>
</template>

<script>
    export default {
        name: "Contact",
        data () {
            return {
                email: "dave@example.com",
                web: "example@example.com"
            }
        }
    }
</script>

<style scoped>
    .noBullets {
        list-style: none;
    }

</style>