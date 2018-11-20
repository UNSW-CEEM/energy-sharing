import * as axios from 'axios';

const BASE_URL = "http://127.0.0.1:5000";

function upload(formData) {
    const url =  `${BASE_URL}/upload`;
    return axios.post(url, formData)
        .then(response => response.data)

        .then(response => response.map(img => Object.assign({},
            img, { url: `${BASE_URL}/solar/${img.id}` })));
}

function uploadTest() {
    const url =  `${BASE_URL}/uploadTest`;

    axios.post(url, {data: "test"})
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        })
}

export { upload }
export { uploadTest }