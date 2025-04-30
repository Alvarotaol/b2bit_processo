// src/services/profile.ts
import Api from "./http";

export async function fetchProfileData(user_id: number | undefined) {
  const response = await Api.get(`/users/profile/${user_id? user_id :''}`);
  return response.data;
}

export async function toggleFollow(user_id: number) {
  const response = await Api.post(`/users/follow/${user_id}/`);
  return response.data;
}

export function loadPosts(user_id: number | string) {
  return Api.get(`/users/${user_id}/posts/`);
}