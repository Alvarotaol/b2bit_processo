import { createContext } from "react";
import { UserType } from "../types";
import useAuth from "../hooks/useAuth";

export const UserContext = createContext({} as UserType);

interface Props {
	children: React.ReactNode;
}

function UserContextProvider({ children }: Props) {
	const { getLoggedUser, user } = useAuth();
	let userData = user;

	if(!userData.id) {
		userData = getLoggedUser();
	}
	return (
		<UserContext.Provider value={userData}>
			{children}
		</UserContext.Provider>
	);
}

export default UserContextProvider;