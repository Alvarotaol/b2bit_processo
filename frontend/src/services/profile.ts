// src/services/profile.ts
import { UserProfileType } from "../types";
import Api from "./http";

export async function fetchProfileData(user_id: number | string | undefined) {
  const response = await Api.get(`/users/profile/${user_id? user_id :''}`);
  return response.data;
}

export async function toggleFollow(user: UserProfileType) {
  if(user.is_following) {
    const response = await Api.post(`/users/unfollow/${user.id}/`);
    return response.status == 200 ? false : undefined;
  }
  const response = await Api.post(`/users/follow/${user.id}/`);
  return response.status == 201 ? true : undefined;
}

export function loadPosts(user_id: number | string) {
  return Api.get(`/users/${user_id}/posts/`);
}