export interface PostType {
	id: number;
	username: string;
	user_id: number;
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

export interface UserProfileType {
	id: number;
	username: string;
	email: string;
	followers_count: number;
	following_count: number;
	is_following?: boolean;
}
