import axios from "axios";

class Api {
	static getAxios (withCredentials: boolean = true) {
		if(withCredentials)
			axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem("token")}`;

		return axios.create({
			baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
			withCredentials,
		});
	}

	static get(url: string, data: object = {}, withCredentials: boolean = true) {
		return this.getAxios(withCredentials).get(url, {
			params: data,
		});
	}

	static post(url: string, data: object = {}, withCredentials: boolean = true) {
		return this.getAxios(withCredentials).post(url, data);
	}

	static delete(url: string, data: object = {}, withCredentials: boolean = true) {
		return this.getAxios(withCredentials).delete(url, data);
	}
}


export default Api;