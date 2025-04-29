export interface PostType {
	id: number;
	user: string;
	text: string;
	created_at: string;
	image?: string;
	like_count: number;
	has_liked?: boolean;
}

export interface UserType {
	id: number;
	username: string;
	email: string;
}
