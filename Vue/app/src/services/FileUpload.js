import * as axios from 'axios';

const BASE_URL = "http://127.0.0.1:5000";

function upload(formData) {
    const url =  `${BASE_URL}/uploadTest`;
    return axios.post(url, formData)
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        });
        // .then(response => response.data)
        //
        // .then(response => response.map(img => Object.assign({},
        //     img, { url: `${BASE_URL}/solar/${img.id}` })));
}

export { upload }