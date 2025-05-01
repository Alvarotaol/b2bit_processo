import axios, { AxiosResponse } from "axios";

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
		}).catch(err => {
			if(err.response.status === 401) {
				window.location.href = "/login";
			}
			return {} as AxiosResponse;
		});
	}

	static post(url: string, data: object | FormData = {}, withCredentials: boolean = true) {
		if(data instanceof FormData) {
			return this.getAxios(withCredentials).post(url, data, {
				headers: {
					"Content-Type": "multipart/form-data"
				}
			}).catch(err => {
				if(err.response.status === 401) {
					window.location.href = "/login";
				}
				if(err.response.status === 429) {
					console.error("Too many requests");
				}
				return {} as AxiosResponse;
			});
		}
		return this.getAxios(withCredentials).post(url, data).catch(err => {
			if(err.response.status === 401) {
				window.location.href = "/login";
			}
			if(err.response.status === 429) {
				console.error("Too many requests");
			}
			return {} as AxiosResponse;
		});
	}

	static delete(url: string, data: object = {}, withCredentials: boolean = true) {
		return this.getAxios(withCredentials).delete(url, data);
	}
}


export default Api;