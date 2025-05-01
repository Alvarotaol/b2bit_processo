import axios, { AxiosResponse } from "axios";

class Api {
	static getAxios (withCredentials: boolean = true) {
		if(withCredentials)
			axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem("token")}`;

		axios.interceptors.response.use(
			(response) => response,
			async (err) => {
				console.log("interceptor", err);
				const originalRequest = err.config;
				if (err.response?.status === 401 && !originalRequest._retry) {
				originalRequest._retry = true;

				try {
					const res = await axios.post("/api/token/refresh/", {
						refresh: localStorage.getItem("refresh"),
					});

					localStorage.setItem("access", res.data.access);
					axios.defaults.headers.common["Authorization"] = `Bearer ${res.data.access}`;
					return axios(originalRequest);
				} catch (refreshError) {
					console.error("Refresh token failed", refreshError);
					window.location.href = "/login";
				}
				}
				return Promise.reject(err);
			}
		);

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
			});
		}
		return this.getAxios(withCredentials).post(url, data);
	}

	static put(url: string, data: object = {}, withCredentials: boolean = true) {
		return this.getAxios(withCredentials).put(url, data);
	}

	static delete(url: string, data: object = {}, withCredentials: boolean = true) {
		return this.getAxios(withCredentials).delete(url, data);
	}
}


export default Api;